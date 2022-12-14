from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from saloonapp.validators import validate_svg_file_extension


class User(AbstractUser):
    phone = PhoneNumberField('контактный номер', region='RU')
    avatar = models.FileField('заглавное фото салона', validators=[validate_svg_file_extension], null=True, blank=True)
