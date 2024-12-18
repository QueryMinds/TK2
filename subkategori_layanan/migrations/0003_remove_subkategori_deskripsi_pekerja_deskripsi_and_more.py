# Generated by Django 5.1.3 on 2024-11-11 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subkategori_layanan', '0002_pekerja_testimoni'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subkategori',
            name='deskripsi',
        ),
        migrations.AddField(
            model_name='pekerja',
            name='deskripsi',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subkategori',
            name='tipe',
            field=models.CharField(choices=[('pengguna', 'Pengguna'), ('pekerja', 'Pekerja')], default='pengguna', max_length=10),
        ),
    ]
