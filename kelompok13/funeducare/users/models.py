from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    # Pilihan untuk jenis kelamin
    GENDER_CHOICES = [
        ('Laki-laki', 'Pria'),
        ('Perempuan', 'Wanita'),
    ]

    # Menambahkan field untuk gender
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    # Field tambahan
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    alamat = models.CharField(max_length=255, null=True, blank=True)
    no_telp = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(unique=True)

    # Override username untuk mengizinkan spasi
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w\s]+$', 
                message='Username hanya boleh mengandung huruf, angka, dan spasi.',
            )
        ],
    )

    # Gunakan email sebagai field login utama
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email

# profile untuk anak
class Child(models.Model):
    GENDER_CHOICES = [
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children')
    nama_anak = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=10, choices=GENDER_CHOICES)
    hobi = models.CharField(max_length=255)
    riwayat_penyakit = models.TextField()
    program = models.CharField(max_length=255)
    usia = models.IntegerField()
    keterangan_tambahan = models.TextField(null=True, blank=True)
    foto_anak = models.ImageField(upload_to='child_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.nama_anak}"
