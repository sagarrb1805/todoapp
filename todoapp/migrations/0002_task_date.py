# Generated by Django 3.2.5 on 2022-08-20 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateField(default='2000-05-04'),
            preserve_default=False,
        ),
    ]
