# Generated by Django 5.1.3 on 2024-11-25 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pemesanan_jasa', '0005_statuspesanan_remove_pemesananjasa_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pemesananjasa',
            name='testimoni_dibuat',
        ),
    ]