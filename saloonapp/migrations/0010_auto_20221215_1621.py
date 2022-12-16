# Generated by Django 3.2.16 on 2022-12-15 13:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('saloonapp', '0009_auto_20221214_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата и время создания записи'),
        ),
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateField(null=True, verbose_name='дата записи'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата и время платежа'),
        ),
    ]