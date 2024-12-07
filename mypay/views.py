from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import psycopg2
from django.conf import settings
from django.http import JsonResponse

@login_required
def mypay(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cursor = conn.cursor()

        # Query untuk mendapatkan saldo dan riwayat transaksi
        query_balance = "SELECT COALESCE(SUM(amount), 0) FROM mypay_transaction;"
        cursor.execute(query_balance)
        balance = cursor.fetchone()[0]

        query_transactions = """
        SELECT id, date, category, amount, description 
        FROM mypay_transaction
        ORDER BY date DESC;
        """
        cursor.execute(query_transactions)
        transactions = cursor.fetchall()

        cursor.close()
        conn.close()

        return render(request, 'mypay/mypay.html', {
            'balance': balance,
            'transactions': transactions,
        })
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "Terjadi kesalahan."})


@login_required
def transaksi(request):
    if request.method == 'POST':
        try:
            category = request.POST.get('category')
            amount = request.POST.get('amount')
            description = request.POST.get('description')

            if not all([category, amount, description]):
                return JsonResponse({"error": "Semua field harus diisi."}, status=400)

            conn = psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT']
            )
            cursor = conn.cursor()

            # Insert data transaksi
            query_insert = """
            INSERT INTO mypay_transaction (date, category, amount, description)
            VALUES (CURRENT_DATE, %s, %s, %s);
            """
            cursor.execute(query_insert, (category, amount, description))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect('mypay:mypay')
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "Terjadi kesalahan."})
    else:
        return render(request, 'mypay/transaksi.html')
