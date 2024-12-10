from midtransclient import Snap
from django.conf import settings

def create_payment_link(pendaftaran):
    snap = Snap(
        is_production=settings.MIDTRANS_IS_PRODUCTION,
        server_key=settings.MIDTRANS_SERVER_KEY,
        client_key=settings.MIDTRANS_CLIENT_KEY
    )
    
    transaction_details = {
        'order_id': f'ORDER-{pendaftaran.id}',
        'gross_amount': pendaftaran.get_price()
    }
    
    item_details = [{
        'id': f'PROGRAM-{pendaftaran.program}',
        'price': pendaftaran.get_price(),
        'quantity': 1,
        'name': dict(pendaftaran.PROGRAM_CHOICES)[pendaftaran.program]
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
    
    snap_response = snap.create_transaction(transaction)
    return snap_response