# Generated by Django 3.2.16 on 2022-12-18 13:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('saloonapp', '0011_alter_note_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата и время создания счета'),
        ),
    ]