# Generated by Django 2.1.5 on 2019-02-15 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrun',
            name='started',
        ),
    ]
