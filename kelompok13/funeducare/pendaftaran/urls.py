# urls.py
from django.urls import path
from pendaftaran import views

app_name = 'pendaftaran'
urlpatterns = [
    path('', views.pendaftaran, name='pendaftaran'),
    path('syarat/', views.syarat, name='syarat'),
    path('cara_mendaftar/', views.cara_mendaftar, name='cara_mendaftar'),
    path('payment-notification/', views.payment_notification, name='payment_notification'),
]