# Generated by Django 4.1 on 2022-09-19 10:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quizApp", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="Results", new_name="Result",),
    ]
