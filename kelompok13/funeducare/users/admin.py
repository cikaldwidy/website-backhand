from django.contrib import admin

# Register your models here.
from .models import CustomUser,Child

admin.site.register(CustomUser)
admin.site.register(Child)