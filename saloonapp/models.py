from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from .validators import validate_svg_file_extension

User = get_user_model()


# index: as is
class Saloon(models.Model):
    name = models.CharField('название', max_length=100)
    address = models.CharField('адрес', max_length=200)
    city = models.CharField('город', max_length=100)
    avatar = models.FileField('заглавное фото салона', validators=[validate_svg_file_extension], null=True, blank=True)
    masters = models.ManyToManyField('Master', through='SaloonMaster')

    class Meta:
        verbose_name = 'салон красоты'
        verbose_name_plural = 'салоны красоты'

    def __str__(self):
        return self.name


class ServiceGroup(models.Model):
    name = models.CharField('название', max_length=200)
    order = models.IntegerField('порядок отображения группы', help_text='чем меньше число, тем раньше')

    class Meta:
        verbose_name = 'группа услуг'
        verbose_name_plural = 'группы услуг'

    def __str__(self):
        return self.name


# index: as is
# service filter: через ServiceGroup
class Service(models.Model):
    name = models.CharField('название', max_length=200)
    avatar = models.FileField('заглавное фото услуги', validators=[validate_svg_file_extension], null=True, blank=True)
    price = models.DecimalField('цена', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    order = models.IntegerField('порядок отображения внутри группы', help_text='чем меньше число, тем раньше')
    group = models.ForeignKey(ServiceGroup, related_name='services', on_delete=models.PROTECT)
    duration_in_minutes = models.PositiveSmallIntegerField(
        'длительность услуги в минутах',
        help_text='чтобы понимать при записи ближайшее свободное время'
    )

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.name


class MasterSpeciality(models.Model):
    name = models.CharField('название', max_length=200)

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'

    def __str__(self):
        return self.name


# index: as is
# service filter: as is
class Master(models.Model):
    first_name = models.CharField('имя мастера', max_length=100)  # if no user
    last_name = models.CharField('фамилия мастера', max_length=100)  # if no user
    rating_image = models.FileField(
        'картинка оценки',
        validators=[validate_svg_file_extension],
        null=True,
        blank=True,
        help_text='Хардкод пока нет реальных отзывов'
    )
    review_count = models.PositiveSmallIntegerField('количество отзывов', help_text='Хардкод пока нет реальных отзывов')
    avatar = models.FileField('фото мастера', validators=[validate_svg_file_extension], null=True, blank=True)
    start_experience_date = models.DateField('дата начала рабочего стажа', help_text='для расчета стажа')
    speciality = models.ForeignKey(MasterSpeciality, related_name='masters', on_delete=models.PROTECT)
    services = models.ManyToManyField(Service)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def work_experience(self):
        # TODO: сделать точнее
        experience = (timezone.now().date() - self.start_experience_date)
        years = experience.days // 365
        if years:
            months = (experience.days % years) // 30
            return f'{years} г. {months} мес.'
        months = experience.days // 30
        return f'{months} мес.'

    class Meta:
        verbose_name = 'мастер'
        verbose_name_plural = 'мастера'

    def __str__(self):
        return f'{self.speciality} {self.first_name} {self.last_name}'


class SaloonMaster(models.Model):
    saloon = models.ForeignKey(Saloon, related_name='masterlinks', on_delete=models.CASCADE)
    master = models.ForeignKey(Master, related_name='saloonlinks', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'расписание мастера по дням недели'
        verbose_name_plural = 'расписания мастера по дням недели'

    def __str__(self):
        return f'{self.saloon} {self.master}'


class SaloonMasterWeekday(models.Model):
    class IsoWeekdays(models.TextChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    isoweekday = models.CharField('день недели по ISO', max_length=9, choices=IsoWeekdays.choices)
    saloonmaster = models.ForeignKey(SaloonMaster, related_name='weekdays', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'рабочий день мастера'
        verbose_name_plural = 'рабочие дни мастера'

    def __str__(self):
        return f'{self.saloonmaster} {self.isoweekday}'


class PaymentType(models.Model):
    name = models.CharField('название', max_length=200)

    class Meta:
        verbose_name = 'тип платежа'
        verbose_name_plural = 'типы платежей'

    def __str__(self):
        return self.name


class Promo(models.Model):
    name = models.CharField('название компании', max_length=200, blank=True)
    description = models.CharField('описание компании', max_length=500, blank=True)
    code = models.CharField('промо код', max_length=20)
    is_active = models.BooleanField('статус активности', default=False)
    percent = models.IntegerField(
        'скидка в процентах',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    absolute = models.IntegerField(
        'абсолютная скидка',
        default=0,
        validators=[MinValueValidator(0)]
    )


class Payment(models.Model):
    class Status(models.TextChoices):
        cancelled = 'Отменен'
        paid = 'Оплачен'
        created = 'Создан'

    user = models.ForeignKey(User, related_name='payments', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField('дата и время создания счета')
    paid_at = models.DateTimeField('дата и время платежа', null=True)
    ptype = models.ForeignKey(PaymentType, related_name='payments', on_delete=models.DO_NOTHING)
    status = models.CharField('статус платежа', max_length=10, choices=Status.choices)

    def get_total_price(self):
        percent = 0
        absolute = 0
        if self.note.promo:
            percent = self.note.promo.percent / 100
            absolute = self.note.promo.absolute
        price = self.note.price * (1 - percent) - absolute
        return max(Decimal(0), price)

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return f'Платеж {self.pk}'


class Note(models.Model):
    user = models.ForeignKey(User, related_name='notes', on_delete=models.DO_NOTHING)
    saloon = models.ForeignKey(Saloon, related_name='notes', on_delete=models.DO_NOTHING, null=True)
    service = models.ForeignKey(Service, related_name='notes', on_delete=models.DO_NOTHING)
    master = models.ForeignKey(Master, related_name='notes', on_delete=models.DO_NOTHING)
    payment = models.OneToOneField(Payment, on_delete=models.DO_NOTHING)
    # TODO: Для отображения цен со скидкой (например 50% для первой) нужно сделать
    # менеджер, который подтянет с актуальными ценами для юзера.
    # На вход менеждеру промокод
    price = models.DecimalField('цена без промо', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    promo = models.ForeignKey(
        Promo,
        related_name='notes',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateField('дата', null=True)
    stime = models.TimeField('время начала', null=True)
    etime = models.TimeField('время окончания', null=True)

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'

    def __str__(self):
        return f'{self.pk} - {self.saloon}, {self.master}, {self.service}'
