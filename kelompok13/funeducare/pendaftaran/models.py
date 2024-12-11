from django.db import models
from django.utils import timezone
from programs.models import Program, Fee
from users.models import Child
from django.conf import settings

class Pendaftaran(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    JENIS_KELAMIN_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'), 
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
     # Menghubungkan nama_ortu ke model User (CustomUser)
    nama_ortu = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="Nama Orang Tua",
        null=True, blank=True
    )
    
    # Menghubungkan nama_anak ke model Child
    nama_anak = models.ForeignKey(
        Child, 
        on_delete=models.CASCADE, 
        verbose_name="Nama Anak",
        blank=True, null=True
    )

    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="Program")
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, verbose_name="Jenis Program")

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'  # Default status adalah 'pending'
    )
    payment_url = models.CharField(max_length=255, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nama_ortu} - {self.nama_anak}"
    
    def get_price(self):
        return self.fee.amount if self.fee else 0