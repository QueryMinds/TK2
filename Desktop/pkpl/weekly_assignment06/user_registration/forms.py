from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from .models import UserProfile
import re

class UserRegistrationForm(forms.Form):
    # Nama: hanya diisi oleh huruf, angka, dan karakter ('.','_','-')
    nama = forms.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._-]+$',
                message='Nama hanya boleh diisi oleh huruf, angka, dan karakter (\'.\',\'_\',\'-\').'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama'})
    )
    
    # Password: huruf, angka, karakter spesial, panjang min 8
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message='Password harus diisi oleh huruf, angka, dan karakter spesial dengan panjang minimal 8.'
            )
        ]
    )
    
    # Tanggal Lahir: usia min 12 tahun
    tanggal_lahir = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    # Nomor HP: hanya angka, panjang 8-15
    nomor_hp = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'cth: 62123456'})
    )
    
    # Email: sesuai format email
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    
    # URL Blog: sesuai format URL
    url_blog = forms.URLField(
        max_length=255,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL Blog'})
    )
    
    # Deskripsi Diri: min 5, max 1000
    deskripsi_diri = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Deskripsi diri', 'rows': 4}),
    )
    
    # Skor Kredit: 0-800
    skor_kredit = forms.IntegerField(
        validators=[
            MinValueValidator(0, message='Skor kredit minimal adalah 0.'),
            MaxValueValidator(800, message='Skor kredit maksimal adalah 800.')
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Skor Kredit'})
    )
    
    # Nomor Kartu ATM: 15-16 digit angka
    nomor_kartu_atm = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor Kartu ATM'})
    )
    
    def clean_tanggal_lahir(self):
        """Validate minimum age is 12 years"""
        tanggal_lahir = self.cleaned_data.get('tanggal_lahir')
        if tanggal_lahir:
            today = date.today()
            age = today.year - tanggal_lahir.year - ((today.month, today.day) < (tanggal_lahir.month, tanggal_lahir.day))
            if age < 12:
                raise ValidationError('Anda harus berusia minimal 12 tahun.')
        return tanggal_lahir
    
    def clean_nomor_hp(self):
        """Sanitize and validate phone number"""
        nomor_hp = self.cleaned_data.get('nomor_hp')
        
        # Sanitize: menghapus karakter + dan - 
        nomor_hp = nomor_hp.replace('+', '').replace('-', '')
        
        # Memvalidasi input hanya terdiri atas 8-15 karakter
        if not re.match(r'^[0-9]{8,15}$', nomor_hp):
            raise ValidationError('Nomor HP harus berupa angka dengan panjang minimal 8 dan maksimal 15.')
        
        return nomor_hp
    
    def clean_deskripsi_diri(self):
        """Validate deskripsi diri length"""
        deskripsi_diri = self.cleaned_data.get('deskripsi_diri')
        if len(deskripsi_diri) < 5:
            raise ValidationError('Deskripsi diri harus memiliki panjang minimal 5 karakter.')
        if len(deskripsi_diri) > 1000:
            raise ValidationError('Deskripsi diri harus memiliki panjang maksimal 1000 karakter.')
        return deskripsi_diri
    
    def clean_nomor_kartu_atm(self):
        """Validate ATM card number"""
        nomor_kartu_atm = self.cleaned_data.get('nomor_kartu_atm')
        if not re.match(r'^[0-9]{15,16}$', nomor_kartu_atm):
            raise ValidationError('Nomor kartu ATM harus terdiri dari 15-16 digit angka.')
        return nomor_kartu_atm