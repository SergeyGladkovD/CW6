# Generated by Django 5.0.7 on 2024-07-30 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": [
                    ("can_block_users", "Can block users"),
                    ("view_all_users", "Can view all users"),
                ],
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
            },
        ),
    ]
