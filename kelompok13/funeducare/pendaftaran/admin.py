from django.contrib import admin
from .models import Pendaftaran

@admin.register(Pendaftaran)
class PendaftaranAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'nama_ortu', 'nama_anak', 'program')
    readonly_fields = ('id', 'created_at')
 