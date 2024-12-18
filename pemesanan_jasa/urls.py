from django.urls import path
from . import views

app_name = 'pemesanan_jasa'

urlpatterns = [
    path('create/<uuid:subkategori_id>/<int:sesi_layanan_id>/', views.create_pemesanan, name='create_pemesanan'),
    path('pemesanan/view/', views.view_pemesanan, name='view_pemesanan'),
    # path('delete/<uuid:pk>/', views.delete_pemesanan, name='batalkan_pesanan'),  # Pastikan ini ada
    path('pemesanan/delete/<uuid:pk>/', views.delete_pemesanan, name='batalkan_pesanan'),  # Make sure this matches
    path('submit_testimonial/', views.submit_testimonial, name='submit_testimonial'),
]
