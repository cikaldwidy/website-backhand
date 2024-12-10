# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import BookingForm
from .models import Pendaftaran
from .utils import create_payment_link
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.conf import settings

def pendaftaran(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            # Buat instance pendaftaran
            pendaftaran = Pendaftaran.objects.create(
                nama_ortu=form.cleaned_data['nama_ortu'],
                email=form.cleaned_data['email'],
                nomor_wa=form.cleaned_data['nomor_wa'],
                alamat=form.cleaned_data['alamat'],
                ktp=request.FILES['ktp'],
                nama_anak=form.cleaned_data['nama_anak'],
                umur_anak=form.cleaned_data['umur_anak'],
                jenis_kelamin=form.cleaned_data['jenis_kelamin'],
                akta_kelahiran=request.FILES['akta_kelahiran'],
                program=form.cleaned_data['program']
            )
            
            # Buat payment link menggunakan Snap
            snap_response = create_payment_link(pendaftaran)
            
            if 'redirect_url' in snap_response:
                pendaftaran.payment_url = snap_response['redirect_url']
                pendaftaran.save()
                
                # Render halaman payment dengan informasi pembayaran
                program_name = dict(pendaftaran.PROGRAM_CHOICES)[pendaftaran.program]
                return render(request, 'payment.html', {
                    'payment_url': snap_response['redirect_url'],
                    'program_name': program_name,
                    'amount': pendaftaran.get_price()
                })
            
            # Jika gagal membuat payment link
            return render(request, 'payment_error.html', {'error': 'Gagal membuat link pembayaran'})
    else:
        form = BookingForm()

    return render(request, 'form_booking.html', {'form_booking': form})

def syarat(request):
    return render(request, 'syarat.html')

def cara_mendaftar(request):
    return render(request, 'cara_mendaftar.html')

@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        notification = json.loads(request.body)
        
        transaction_status = notification['transaction_status']
        order_id = notification['order_id']
        
        # Get pendaftaran ID from order_id
        pendaftaran_id = order_id.replace('ORDER-', '')
        try:
            pendaftaran = Pendaftaran.objects.get(id=pendaftaran_id)
            
            if transaction_status == 'settlement':
                pendaftaran.payment_status = 'paid'
            elif transaction_status == 'pending':
                pendaftaran.payment_status = 'pending'
            elif transaction_status in ['deny', 'cancel', 'expire']:
                pendaftaran.payment_status = 'failed'
                
            pendaftaran.save()
            return HttpResponse(status=200)
        except Pendaftaran.DoesNotExist:
            return HttpResponse(status=404)
            
    return HttpResponse(status=400)
