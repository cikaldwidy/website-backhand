from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'users'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('pengaturanakun/', views.update_account, name='pengaturanakun'),
    path('programaktif/', views.program_aktif, name='programaktif'),
    path('riwayatkegiatan/', views.riwayat_kegiatan, name='riwayatkegiatan'),
    path('laporanperkembangan/', views.laporan_perkembangan, name='laporanperkembangan'),
    path('riwayat-pembayaran/', views.riwayat_pembayaran, name='riwayat_pembayaran'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('children/<int:child_id>/delete/', views.delete_child, name='delete_child'),

    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    ),
]