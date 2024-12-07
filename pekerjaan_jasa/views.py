import psycopg2
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib import messages

from TK2.pekerjaan_jasa.forms import ServiceOrderForm

@login_required
def pekerjaan_jasa(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cursor = conn.cursor()

        selected_category = request.GET.get('category')
        selected_subcategory = request.GET.get('subcategory')

        # Query SQL untuk mendapatkan pekerjaan yang relevan
        query = """
        SELECT o.id, o.tgl_pemesanan, o.total_biaya, sk.nama_subkategori AS subkategori
        FROM pekerjaan_jasa_serviceorder o
        JOIN pekerjaan_jasa_servicesubcategory sk ON o.subkategori_id = sk.id
        WHERE o.status = 'mencari'
        """
        params = []

        if selected_category:
            query += " AND sk.kategori_id = %s"
            params.append(selected_category)

        if selected_subcategory:
            query += " AND sk.id = %s"
            params.append(selected_subcategory)

        cursor.execute(query, tuple(params))
        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        return render(request, 'pekerjaan_jasa/urutan_pekerjaan.html', {'orders': orders})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "Terjadi kesalahan."})


    
@login_required
def job_status(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cursor = conn.cursor()

        selected_category = request.GET.get('category')
        selected_subcategory = request.GET.get('subcategory')

        query = """
        SELECT o.id, o.tgl_pemesanan, o.total_biaya, o.status, sk.nama_subkategori AS subkategori
        FROM pekerjaan_jasa_serviceorder o
        JOIN pekerjaan_jasa_servicesubcategory sk ON o.subkategori_id = sk.id
        WHERE o.status != 'dibatalkan'
        """
        params = []

        if selected_category:
            query += " AND sk.kategori_id = %s"
            params.append(selected_category)

        if selected_subcategory:
            query += " AND sk.id = %s"
            params.append(selected_subcategory)

        cursor.execute(query, tuple(params))
        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        return render(request, 'pekerjaan_jasa/status_pekerjaan.html', {'orders': orders})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "Terjadi kesalahan."})


@login_required
def update_status(request, order_id, new_status):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cursor = conn.cursor()

        valid_transitions = {
            "menunggu": "tiba",
            "tiba": "dilakukan",
            "dilakukan": "selesai",
        }

        cursor.execute("SELECT status FROM pekerjaan_jasa_serviceorder WHERE id = %s;", (order_id,))
        current_status = cursor.fetchone()[0]

        if valid_transitions.get(current_status) != new_status:
            return JsonResponse({"error": "Transisi status tidak valid."})

        update_query = "UPDATE pekerjaan_jasa_serviceorder SET status = %s WHERE id = %s;"
        cursor.execute(update_query, (new_status, order_id))
        conn.commit()

        cursor.close()
        conn.close()

        return JsonResponse({"success": "Status pekerjaan berhasil diperbarui."})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "Terjadi kesalahan."})

@login_required
def get_subcategories(request, category_id):
    try:
        # Koneksi ke database dan menjalankan query SQL untuk mendapatkan subkategori
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cursor = conn.cursor()

        query = """
        SELECT id, nama_subkategori
        FROM pekerjaan_jasa_servicesubcategory
        WHERE kategori_id = %s
        """
        cursor.execute(query, (category_id,))
        subcategories = cursor.fetchall()

        cursor.close()
        conn.close()

        # Kirimkan data subkategori dalam format JSON
        subcategory_data = [{"id": sub[0], "name": sub[1]} for sub in subcategories]
        return JsonResponse(subcategory_data, safe=False)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "Terjadi kesalahan."})

def accept_order(request, order_id):
    try:
        # Mengambil pesanan berdasarkan order_id
        order = get_object_or_404(ServiceOrderForm, id=order_id)
    except ServiceOrderForm.DoesNotExist:
        raise Http404("Order not found")
    
    # Pastikan hanya pekerja yang dapat menerima pesanan
    if not request.user.is_worker:
        messages.error(request, "You are not authorized to accept orders.")
        return redirect('pekerjaan_jasa:pekerjaan_jasa')

    # Perbarui status dan tetapkan pekerja untuk pesanan
    order.status = 'menunggu'
    order.assigned_worker = request.user
    order.save()

    # Berikan pesan sukses dan arahkan kembali ke halaman pekerjaan
    messages.success(request, "Pesanan berhasil diterima.")
    return redirect('pekerjaan_jasa:pekerjaan_jasa')


