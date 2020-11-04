# Generated by Django 3.1.2 on 2020-10-25 10:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20201019_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.position'),
        ),
        migrations.AlterField(
            model_name='region',
            name='postman',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.employee'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateField(default=datetime.date(2020, 11, 24), verbose_name='Subscription end'),
        ),
    ]
