from django.db import models
from django.utils import timezone

NULLABLE = {"blank": "True", "null": "True"}

STATUS_CHOICES = [
    ("start", "start"),
    ("finish", "finish"),
    ("created", "created"),
]
INTERVAL_CHOICES = [
    ("once_a_day", "once_a_day"),
    ("once_a_week", "once_a_week"),
    ("once_a_month", "once_a_month"),
]


class Client(models.Model):
    email = models.EmailField(max_length=100, unique=True, verbose_name="Почта")
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    def __str__(self):
        return f"{self.email} {self.full_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    topic_letter = models.CharField(max_length=100, verbose_name="Тема письма")
    body_letter = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return f"{self.topic_letter} {self.body_letter}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Время начала рассылки")
    next_date = models.DateTimeField(default=timezone.now, verbose_name="Время следующей рассылки")
    end_date = models.DateTimeField(default=None, verbose_name="Время окончания рассылки")
    period = models.CharField(choices=INTERVAL_CHOICES, max_length=100, default=INTERVAL_CHOICES[0][0], verbose_name="Периуд")
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default=STATUS_CHOICES[0][0], verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, verbose_name="Клиенты")

    def __str__(self):
        return f'{self.start_date} {self.period} {self.next_date} {self.end_date} {self.status} {self.message}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingStatus(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now_add=True, verbose_name="Время последней попытки")
    status_mailing = models.CharField(max_length=100,  verbose_name="Статус попытки")
    response_mailing = models.TextField(verbose_name="Ответ сервера", **NULLABLE)

    def __str__(self):
        return f'{self.last_mailing_time} {self.status_mailing} {self.response_mailing}'

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытка рассылок"
