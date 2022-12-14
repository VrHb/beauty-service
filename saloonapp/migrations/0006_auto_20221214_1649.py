# Generated by Django 3.2.16 on 2022-12-14 13:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('saloonapp', '0005_auto_20221214_1429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='order',
            new_name='payment',
        ),
        migrations.AddField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('Отменен', 'Cancelled'), ('Оплачен', 'Paid'), ('Создан', 'Created')], max_length=10, verbose_name='статус платежа'),
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isoweekday', models.PositiveSmallIntegerField(help_text='Понедельник 1, Воскресенье 7', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)], verbose_name='день недели по ISO')),
                ('date', models.DateField(blank=True, help_text='Заполняется если время занято', null=True, verbose_name='дата')),
                ('stime', models.TimeField(verbose_name='время начала')),
                ('etime', models.TimeField(verbose_name='время окончания')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='timeslots', to='saloonapp.master')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='timeslots', to='saloonapp.saloon')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='timeslots', to='saloonapp.service')),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='timeslot',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='saloonapp.timeslot'),
        ),
    ]
