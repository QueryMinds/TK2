from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

from django.shortcuts import redirect
from .models import Transaction

@login_required
def mypay(request):
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    balance = sum(
        trans.amount if trans.category in ['topup'] else -trans.amount
        for trans in user_transactions
    )

    context = {
        'balance': balance,
        'transactions': user_transactions,
        # 'phone_number': request.user.profile.phone_number  # Pastikan ada field phone_number di profile user
    }
    return render(request, 'mypay/mypay.html', context)

@login_required
def transaksi(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        amount = float(request.POST.get('topupAmount', 0) or
                       request.POST.get('transferAmount', 0) or
                       request.POST.get('withdrawAmount', 0))

        # Simpan transaksi
        Transaction.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=request.POST.get('description', '')  # Opsional
        )
        return redirect('mypay:view')

    return render(request, 'mypay/transaksi.html')
