# Generated by Django 3.2.16 on 2022-12-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saloonapp', '0013_alter_payment_ptype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='services',
            field=models.ManyToManyField(related_name='masters', to='saloonapp.Service'),
        ),
    ]
