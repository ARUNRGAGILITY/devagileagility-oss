# Generated by Django 4.2 on 2023-07-04 06:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_todolist', '0003_newtodolist_workitemtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='newtodolist',
            name='description',
            field=models.TextField(default=datetime.datetime(2023, 7, 4, 6, 18, 58, 461856, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]