import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import connection
from authentication.views import login_required
import psycopg2
from authentication.views import get_user
from django.contrib import messages
from django.urls import reverse

@login_required
def mypay(request):
   user = get_user(request)
   if not user['logged_in']:
       return redirect('authentication:login')

   try:
       with connection.cursor() as cursor:
           # Ambil riwayat transaksi
           cursor.execute("""
               SELECT date, category, amount, description
               FROM mypay_transaction
               ORDER BY date DESC;
           """)
           transactions = cursor.fetchall()

           # Ambil saldo user dari tabel USER
           cursor.execute("""
               SELECT saldo 
               FROM "USER"
               WHERE id = %s;
           """, [user['id']])
           balance = cursor.fetchone()[0]

   except Exception as e:
       balance = 0.0
       transactions = []
       print(f"Error: {e}")

   return render(request, 'mypay/mypay.html', {
       'balance': balance,
       'transactions': transactions,
       'user': user,
   })

@login_required
def transaksi(request):
   user = get_user(request)
   if not user['logged_in']:
       return redirect('authentication:login')

   if request.method == "POST":
       try:
           category = request.POST.get('category')
           amount = None
           description = None

           # Process based on category
           if category == "TopUp":
               amount = request.POST.get('amount_topup')
               description = "TopUp pertama"
               
               if not amount:
                   return render(request, 'mypay/transaksi.html', {
                       'error': 'Nominal top up harus diisi',
                       'user': user
                   })
               
               amount = float(amount)
               
               with connection.cursor() as cursor:
                   cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM mypay_transaction")
                   next_id = cursor.fetchone()[0]

                   cursor.execute("""
                       INSERT INTO mypay_transaction 
                       (id, date, category, amount, description)
                       VALUES (%s, CURRENT_DATE, %s, %s, %s)
                   """, [next_id, category, amount, description])
                   
                   cursor.execute("""
                       UPDATE "USER" 
                       SET saldo = saldo + %s 
                       WHERE id = %s
                   """, [amount, user['id']])

                   connection.commit()
                   
                   return redirect(f"{reverse('mypay:view')}?success=true")

           elif category == "Transfer":
               amount = request.POST.get('amount')
               target = request.POST.get('description')
               if not amount or not target:
                   return render(request, 'mypay/transaksi.html', {
                       'error': 'Nomor HP tujuan dan nominal transfer harus diisi',
                       'user': user
                   })
               description = f"Transfer ke {target}"
               amount = float(amount)
               
               with connection.cursor() as cursor:
                   cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM mypay_transaction")
                   next_id = cursor.fetchone()[0]
                   
                   cursor.execute("""
                       INSERT INTO mypay_transaction 
                       (id, date, category, amount, description)
                       VALUES (%s, CURRENT_DATE, %s, %s, %s)
                   """, [next_id, category, -amount, description])
                   
                   cursor.execute("""
                       UPDATE "USER" 
                       SET saldo = saldo - %s 
                       WHERE id = %s
                   """, [amount, user['id']])
                   
                   connection.commit()
                   return redirect(f"{reverse('mypay:view')}?success=true")

           elif category == "Bayar Jasa":
               service = request.POST.get('description')
               amount = 150000  # Fixed amount
               description = f"Pembayaran jasa {service}"
               
               with connection.cursor() as cursor:
                   cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM mypay_transaction")
                   next_id = cursor.fetchone()[0]
                   
                   cursor.execute("""
                       INSERT INTO mypay_transaction 
                       (id, date, category, amount, description)
                       VALUES (%s, CURRENT_DATE, %s, %s, %s)
                   """, [next_id, category, amount, description])
                   
                   cursor.execute("""
                       UPDATE "USER" 
                       SET saldo = saldo - %s 
                       WHERE id = %s
                   """, [amount, user['id']])
                   
                   connection.commit()
                   return redirect(f"{reverse('mypay:view')}?success=true")
                   
           elif category == "Withdrawal":
               amount = request.POST.get('amount')
               bank = request.POST.get('description')
               if not amount or not bank:
                   return render(request, 'mypay/transaksi.html', {
                       'error': 'Bank tujuan dan nominal penarikan harus diisi',
                       'user': user
                   })
               description = f"Penarikan saldo MyPay ke {bank}"
               amount = float(amount)
               
               with connection.cursor() as cursor:
                   cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM mypay_transaction")
                   next_id = cursor.fetchone()[0]
                   
                   cursor.execute("""
                       INSERT INTO mypay_transaction 
                       (id, date, category, amount, description)
                       VALUES (%s, CURRENT_DATE, %s, %s, %s)
                   """, [next_id, category, -amount, description])
                   
                   cursor.execute("""
                       UPDATE "USER" 
                       SET saldo = saldo - %s 
                       WHERE id = %s
                   """, [amount, user['id']])
                   
                   connection.commit()
                   return redirect(f"{reverse('mypay:view')}?success=true")
                   
           else:
               return render(request, 'mypay/transaksi.html', {
                   'error': 'Kategori transaksi tidak valid',
                   'user': user
               })

       except Exception as e:
           print(f"Error in transaction: {e}")
           return render(request, 'mypay/transaksi.html', {
               'error': f'Terjadi kesalahan: {str(e)}',
               'user': user
           })

   return render(request, 'mypay/transaksi.html', {'user': user})