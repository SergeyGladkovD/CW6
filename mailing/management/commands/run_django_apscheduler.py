import logging
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing, MailingStatus

logger = logging.getLogger(__name__)


def my_job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, "interval", seconds=30)
    scheduler.start()


def send_mailing():
    day = timedelta(days=1, hours=0, minutes=0)
    weak = timedelta(days=7, hours=0, minutes=0)
    month = timedelta(days=30, hours=0, minutes=0)
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(
        zone
    )  # Получаем текущее дату и время с учетом таймзоны.
    # создание объекта с применением фильтра
    mailings = Mailing.objects.filter(
        status="created",
        start_date__lte=current_datetime,
        end_date__gte=current_datetime,
    )

    for mailing in mailings:  # Отправляем рассылку всем клиентам.
        mailing.status = "start"
        mailing.save()
        server_response = send_mail(
            subject=mailing.message.topic_letter,
            message=mailing.message.body_letter,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.client.all()],
            fail_silently=False,
        )
        if server_response:
            status = "Отправлено"
        else:
            status = "Ошибка отправки"

        log = MailingStatus(response_mailing=mailing, status_mailing=status)
        log.save()  # Записываем лог нашей рассылки.
        # Проверяем периодичность рассылки и соответствие текущей даты и даты старта рассылки.
        if mailing.period == "once_a_day":
            mailing.next_date = log.last_mailing_time + day
        elif mailing.period == "once_a_week":
            mailing.next_date = log.last_mailing_time + weak
        elif mailing.period == "once_a_month":
            mailing.next_date = log.last_mailing_time + month

        if mailing.next_date < mailing.end_date:
            mailing.status = "created"
        else:
            mailing.status = "finish"
        mailing.save()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
