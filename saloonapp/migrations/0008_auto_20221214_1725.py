# Generated by Django 3.2.16 on 2022-12-14 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saloonapp', '0007_auto_20221214_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaloonMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saloonlinks', to='saloonapp.master')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masterlinks', to='saloonapp.saloon')),
            ],
            options={
                'verbose_name': 'расписание мастера по дням недели',
                'verbose_name_plural': 'расписания мастера по дням недели',
            },
        ),
        migrations.CreateModel(
            name='SaloonMasterWeekday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isoweekday', models.CharField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], max_length=9, verbose_name='день недели по ISO')),
                ('saloonmaster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekdays', to='saloonapp.saloonmaster')),
            ],
            options={
                'verbose_name': 'рабочий день мастера',
                'verbose_name_plural': 'рабочие дни мастера',
            },
        ),
        migrations.RemoveField(
            model_name='note',
            name='timeslot',
        ),
        migrations.AddField(
            model_name='note',
            name='date',
            field=models.DateField(null=True, verbose_name='дата'),
        ),
        migrations.AddField(
            model_name='note',
            name='etime',
            field=models.TimeField(null=True, verbose_name='время окончания'),
        ),
        migrations.AddField(
            model_name='note',
            name='stime',
            field=models.TimeField(null=True, verbose_name='время начала'),
        ),
        migrations.DeleteModel(
            name='TimeSlot',
        ),
        migrations.AddField(
            model_name='saloon',
            name='masters',
            field=models.ManyToManyField(through='saloonapp.SaloonMaster', to='saloonapp.Master'),
        ),
    ]
