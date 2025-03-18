from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_minimum_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 12:
        raise ValidationError(_('Anda harus berusia minimal 12 tahun.'))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tanggal_lahir = models.DateField(validators=[validate_minimum_age])
    
    # Nomor HP: hanya angka, panjang 8-15
    nomor_hp = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{8,15}$',
                message='Nomor HP harus berupa angka dengan panjang minimal 8 dan maksimal 15.'
            )
        ]
    )
    
    url_blog = models.URLField(max_length=255)
    
    # Deskripsi diri: min 5, max 1000
    deskripsi_diri = models.TextField(
        validators=[
            RegexValidator(
                regex=r'^.{5,1000}$',
                message='Deskripsi diri harus memiliki panjang antara 5 hingga 1000 karakter.'
            )
        ]
    )
    
    # Skor Kredit: 0-800
    skor_kredit = models.IntegerField(
        validators=[
            MinValueValidator(0, message='Skor kredit minimal adalah 0.'),
            MaxValueValidator(800, message='Skor kredit maksimal adalah 800.')
        ]
    )
    
    # Nomor Kartu ATM: 15-16 digit angka
    nomor_kartu_atm = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{15,16}$',
                message='Nomor kartu ATM harus terdiri dari 15-16 digit angka.'
            )
        ]
    )
    
    def __str__(self):
        return self.user.username