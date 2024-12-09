import psycopg2
from django.conf import settings
from django.shortcuts import render, redirect
from authentication.views import get_user, login, login_required
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    logger.info("Homepage function called") 
    print("Kepanggil nih homepage")
    try:
        # Koneksi manual ke database menggunakan psycopg2
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres.cvcodnolmjlcawbfcebn',
            password='KYX-6ri@DN8Q.wc',
            host='aws-0-us-east-1.pooler.supabase.com',
            port='5432',
        )
        cursor = conn.cursor()

        # Query kategori
        cursor.execute("SELECT id, nama_kategori FROM kategori_jasa")
        kategori_list = cursor.fetchall()

        # Query subkategori
        cursor.execute("""
            SELECT s.id, s.nama, s.kategori_id, s.tipe
            FROM subkategori_layanan_subkategori s
        """)
        subkategori_list = cursor.fetchall()

        # Tutup koneksi database
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error saat menjalankan query:", e)
        return render(request, 'error_page.html', {'message': 'Error saat menjalankan query.'})

    # Tentukan role pengguna berdasarkan is_pengguna dan is_pekerja
    is_pengguna = request.user.is_pengguna
    is_pekerja = request.user.is_pekerja

    # Debugging role
    print(f"User: {request.user}, Is Pengguna: {is_pengguna}, Is Pekerja: {is_pekerja}")
    print(f"User: {request.user}, Is Pengguna: {getattr(request.user, 'is_pengguna', False)}, Is Pekerja: {getattr(request.user, 'is_pekerja', False)}")

    # Render data ke template
    return render(request, 'homepage.html', {
        'kategori_list': kategori_list,
        'subkategori_list': subkategori_list,
        'is_pengguna': is_pengguna,
        'is_pekerja': is_pekerja,
    })

    # Me-retreive user yang aktif
    user = get_user(request)
    print(user)
    # Mengirim data ke template
    return render(request, 'homepage.html', {'subkategori_list': subkategori_list, 'user': user})

def not_logged_in(request):
    if request.session.get('phone_number', 'not found') != 'not found' or request.session.get('is_pekerja', 'not found') != 'not found' or request.session.get('user_id' ,'not found') != 'not found':
        print(request.session['phone_number'], request.session['is_pekerja'], request.session['user_id'])
        return redirect('homepage')
    else:
        return render(request, 'not_logged_in.html')
