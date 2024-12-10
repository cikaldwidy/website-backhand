import uuid
from midtransclient import Snap
from django.conf import settings
import json
from decimal import Decimal

def create_payment_link(pendaftaran):
    snap = Snap(
        is_production=settings.MIDTRANS_IS_PRODUCTION,
        server_key=settings.MIDTRANS_SERVER_KEY,
        client_key=settings.MIDTRANS_CLIENT_KEY
    )
    
    # Menggunakan UUID untuk membuat order_id yang unik
    order_id = f'ORDER-{str(uuid.uuid4())}'  # UUID menjamin keunikan
    
    gross_amount = float(pendaftaran.get_price())  # Konversi Decimal ke float
    
    # Pastikan gross_amount lebih besar dari 0
    if gross_amount <= 0:
        raise ValueError("Gross amount should be greater than 0")
    
    transaction_details = {
        'order_id': order_id,  # Gunakan order_id yang unik
        'gross_amount': gross_amount
    }
    
    item_details = [{
        'id': f'PROGRAM-{pendaftaran.program.id}',  # Mengakses id program
        'price': gross_amount,  # Konversi Decimal ke float
        'quantity': 1,
        'name': pendaftaran.program.name  # Mengakses nama program langsung dari model Program
    }]
    
    customer_details = {
        'first_name': pendaftaran.nama_ortu,
        'email': pendaftaran.email,
        'phone': pendaftaran.nomor_wa
    }
    
    transaction = {
        'transaction_details': transaction_details,
        'item_details': item_details,
        'customer_details': customer_details
    }
    
    try:
        snap_response = snap.create_transaction(transaction)
        # Update the payment status based on the response from Midtrans
        pendaftaran.payment_status = 'pending'  # Initial status is 'pending'
        
        # Check the transaction status from the response
        if snap_response['transaction_status'] == 'capture' or snap_response['transaction_status'] == 'settlement':
            pendaftaran.payment_status = 'success'
        elif snap_response['transaction_status'] == 'deny' or snap_response['transaction_status'] == 'expire':
            pendaftaran.payment_status = 'failed'
        
        # Save the status to the database
        pendaftaran.save()
        
        return snap_response
    except Exception as e:
        print(f"Error while creating payment link: {str(e)}")
        pendaftaran.payment_status = 'failed'  # In case of error, mark it as failed
        pendaftaran.save()
        return None


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
