# Generated by Django 3.1.2 on 2020-10-28 14:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20201025_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='post_office',
        ),
        migrations.AddField(
            model_name='release',
            name='post_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.postoffice'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateField(default=datetime.date(2020, 11, 27), verbose_name='Subscription end'),
        ),
    ]
