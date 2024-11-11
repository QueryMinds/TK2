# Generated by Django 5.1.3 on 2024-11-11 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_pekerja_gender'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pekerja',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='pekerja',
            constraint=models.UniqueConstraint(fields=('bank', 'bank_number'), name='bank constraint'),
        ),
    ]
