from midtransclient import Snap
from django.conf import settings
import json
import uuid
import requests
from .models import Pendaftaran

def create_payment_link(pendaftaran):
    snap = Snap(
        is_production=settings.MIDTRANS_IS_PRODUCTION,
        server_key=settings.MIDTRANS_SERVER_KEY,
        client_key=settings.MIDTRANS_CLIENT_KEY
    )
    
    # Buat order_id unik dengan UUID
    order_id = f'ORDER-{str(uuid.uuid4())}'

    transaction_details = {
        'order_id': order_id,  
        'gross_amount': float(pendaftaran.get_price())  
    }
    
    item_details = [{
        'id': f'PROGRAM-{pendaftaran.program.id}',  # Program ID
        'price': float(pendaftaran.get_price()),  # Konversi Decimal ke float
        'quantity': 1,
        'name': pendaftaran.program.name  # Program name
    }]
    
    customer_details = {
        'first_name': pendaftaran.nama_ortu.first_name,  # Parent's first name
        'email': pendaftaran.nama_ortu.email,  # Parent's email
        'child_name': pendaftaran.nama_anak.nama_anak,  # Child's name
        'program': pendaftaran.program.name,  # Program name
    }
    
    transaction = {
        'transaction_details': transaction_details,
        'item_details': item_details,
        'customer_details': customer_details
    }

    snap_response = snap.create_transaction(transaction)
    
    # Update Pendaftaran dengan payment_url dan order_id
    pendaftaran.payment_url = snap_response['redirect_url']
    pendaftaran.order_id = order_id  # Menyimpan order_id ke dalam model Pendaftaran
    pendaftaran.payment_status = 'pending'  # Status awal adalah 'pending'
    pendaftaran.save()

    return snap_response


def check_payment_status(order_id):
    # URL endpoint untuk cek status pembayaran
    url = f"https://api.midtrans.com/v2/{order_id}/status"
    
    # Header dengan authorization menggunakan server key
    headers = {
        'Authorization': f'Basic {settings.MIDTRANS_SERVER_KEY}',
        'Content-Type': 'application/json'
    }

    # Kirim request GET ke Midtrans API untuk mendapatkan status pembayaran
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        payment_status = data.get('transaction_status', None)

        try:
            pendaftaran = Pendaftaran.objects.get(order_id=order_id)
            pendaftaran.payment_status = payment_status
            pendaftaran.save()
            return payment_status
        except Pendaftaran.DoesNotExist:
            return None
    else:
        return f"Error: {response.status_code}, {response.text}"
