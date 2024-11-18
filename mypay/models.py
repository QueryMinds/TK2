from django.conf import settings
from django.db import models

class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('topup', 'Top Up MyPay'),
        ('jasa', 'Bayar Jasa'),
        ('transfer', 'Transfer MyPay'),
        ('withdrawal', 'Withdrawal'),
    ]

    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
