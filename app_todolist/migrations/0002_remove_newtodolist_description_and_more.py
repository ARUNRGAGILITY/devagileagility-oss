# Generated by Django 4.2 on 2023-04-10 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_todolist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newtodolist',
            name='description',
        ),
        migrations.RemoveField(
            model_name='newtodolist',
            name='priority',
        ),
    ]