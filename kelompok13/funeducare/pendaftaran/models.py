from django.db import models
from django.utils import timezone

class Pendaftaran(models.Model):
    # Tambahkan field id dan created_at
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    JENIS_KELAMIN_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'), 
    ]

    PROGRAM_CHOICES = [
        ('infant', 'Infant Care (0-12 bulan)'),
        ('toddler', 'Toddler Program (1-2 tahun)'),
        ('preschool', 'Pre-school Program (3-4 tahun)'),
        ('prekindergarten', 'Pre-kindergarten (4-5 tahun)'),
    ]

    nama_ortu = models.CharField(max_length=100, verbose_name="Nama Orang Tua")
    email = models.EmailField(verbose_name="Alamat Email")
    nomor_wa = models.CharField(max_length=15, verbose_name="Nomor WhatsApp Orang Tua")
    alamat = models.TextField(verbose_name="Alamat Orang Tua")
    ktp = models.FileField(upload_to='uploads/ktp/', verbose_name="Upload KTP Orang Tua")
    nama_anak = models.CharField(max_length=100, verbose_name="Nama Anak")
    umur_anak = models.CharField(max_length=2, verbose_name="Umur Anak")
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN_CHOICES, verbose_name="Jenis Kelamin")
    akta_kelahiran = models.FileField(upload_to='uploads/akta_kelahiran/', verbose_name="Upload Akta Kelahiran Anak")
    program = models.CharField(max_length=15, choices=PROGRAM_CHOICES, verbose_name="Program")

    def __str__(self):
        return f"{self.nama_ortu} - {self.nama_anak}"
    
    # Tambahkan field payment
    payment_status = models.CharField(max_length=20, default='pending')
    payment_url = models.CharField(max_length=255, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Tambahkan field harga sesuai program
    def get_price(self):
        prices = {
            'infant': 1500000,
            'toddler': 2000000,
            'preschool': 2500000,
            'prekindergarten': 3000000,
        }
        return prices.get(self.program, 0)
