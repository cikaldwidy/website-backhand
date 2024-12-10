from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import  login,logout
from .forms import SignupForm,LoginForm,ChangePasswordUserForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Child
from .forms import ChildProfileForm


@login_required
def user_logout(request):
    logout(request)
    next_url = request.GET.get('next', '/')  # Jika ada next di URL, arahkan ke halaman tersebut
    return redirect(next_url)  



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save() 
            email = form.cleaned_data['email'] 
            name = form.cleaned_data['username']
            login_url = request.build_absolute_uri('/users/login/')
            send_mail(
            'Selamat, Registrasi Sukses!',
            f'Halo {name},\n\nTerima kasih telah bergabung dengan FunEduCare! Akun Anda berhasil dibuat dan Anda sudah siap memulai petualangan belajar bersama kami.\n\nUntuk mengakses layanan kami dan melanjutkan, silakan login ke akun Anda dengan mengklik tautan berikut:\n{login_url}\n\nJika Anda mengalami kendala saat mengakses akun atau memiliki pertanyaan lebih lanjut, silakan hubungi kami di funeducare.id@gmail.com.\n\nSelamat bergabung dan selamat belajar!',
            'funeducare.id@gmail.com', #email funeducare
            [email],  # Email tujuan 
            fail_silently=False,
)
            messages.success(request, 'Pendaftaran berhasil ! Silakan login.')
        else:
            messages.error(request, 'Ada kesalahan saat pengisian form. Mohon isi ulang kembali !')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  
        if form.is_valid():  # form valid ( validasi captcha)
            user = form.get_user() 
            login(request, user)  # Login user ke session
            messages.success(request, f'Selamat datang {request.user.username} ! Sekarang kamu bagian dari keluarga Funeducare.id') 
            return redirect('home:home')  # Redirect ke halaman home setelah login berhasil
        else:
            print(form.errors)  
            if form.errors.get('captcha'):  # Jika ada error di captcha
                messages.error(request, 'reCAPTCHA tidak valid. Pastikan Anda sudah mengisi reCAPTCHA dengan benar.')
            else:
                messages.error(request, 'Email atau password anda salah. Mohon isi ulang kembali')
            return redirect('users:login')  #  form tidak valid, redirect ke halaman login
    else:
        form = LoginForm() 
    
    return render(request, 'login.html', {'form': form})



def change_password(request):
    form = ChangePasswordUserForm(request.user, request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, 'Password berhasil diganti ! silahkan login kembali')
            return redirect('users:login')  
        else:
            messages.error(request, 'Password tidak valid, silahkan coba lagi !')
            return redirect('users:change_password')
    
    else:
        form = ChangePasswordUserForm(request.user)
    
    context = {
        'judul': 'Change password',
        'form': form,
    }
    return render(request, 'change_password.html', context)


@login_required
def update_account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            # Get cleaned data from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            alamat = form.cleaned_data.get('alamat', request.user.alamat)
            no_telp = form.cleaned_data.get('no_telp', request.user.no_telp)
            gender = form.cleaned_data.get('gender', request.user.gender)

            changes_made = False

            if request.user.username != username:
                request.user.username = username
                changes_made = True
            if request.user.first_name != first_name:
                request.user.first_name = first_name
                changes_made = True
            if request.user.last_name != last_name:
                request.user.last_name = last_name
                changes_made = True
            if request.user.alamat != alamat:
                request.user.alamat = alamat
                changes_made = True

            # Validasi nomor telepon
            if request.user.no_telp != no_telp:
                if no_telp:  # Jika nomor telepon diisi
                    try:
                        # Validator untuk nomor telepon
                        validator = RegexValidator(
                            regex=r'^\+?1?\d{9,12}$',
                            message="Nomor telepon harus terdiri dari 9-12 digit dan hanya angka."
                        )
                        validator(no_telp)
                        request.user.no_telp = no_telp
                        changes_made = True
                    except ValidationError as e:
                        messages.error(request, f"Kesalahan pada nomor telepon: {e.message}")
                        return render(request, 'pengaturan_akun.html', {'form': form})  # Render ulang dengan form dan error

            if request.user.gender != gender:
                request.user.gender = gender
                changes_made = True

            if form.cleaned_data.get('profile_image'):
                if request.user.profile_image != form.cleaned_data['profile_image']:
                    request.user.profile_image = form.cleaned_data['profile_image']
                    changes_made = True

            if 'delete_image' in request.POST and request.POST['delete_image'] == 'on':
                if request.user.profile_image:
                    request.user.profile_image = None
                    changes_made = True

            if changes_made:
                request.user.save()
                messages.success(request, "Akun berhasil diperbarui")
            else:
                messages.info(request, "Tidak ada perubahan yang dilakukan.")

            return redirect('users:pengaturanakun')
        else:
            if form.errors.get('username'):
                messages.error(request, "Username sudah digunakan! Silakan coba lagi.")
    else:
        form = UserUpdateForm(initial={
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'alamat': request.user.alamat,
            'no_telp': request.user.no_telp,
            'gender': request.user.gender,
        }, user=request.user)

    return render(request, 'pengaturan_akun.html', {'form': form})

def profile_view(request, child_id=None):
    form = ChildProfileForm()
    context = {
        'form': form,
    }

    return render(request, 'profil_anak.html', context)

def profile(request, child_id=None):
    children = Child.objects.filter(user=request.user)
    child = None
    form = ChildProfileForm()
    if child_id:
        # If child_id is provided, find and edit the child
        child = get_object_or_404(Child, id=child_id, user=request.user)
        
        if request.method == 'POST' and 'delete' in request.POST:
            # Handle delete operation
            child.delete()
            return redirect('users:profile')  # Redirect back to the profile view

        # If editing, load the form with the child's data
        form = ChildProfileForm(request.POST or None, request.FILES or None, instance=child)

    # Handle the creation or updating of a child profile
    if request.method == 'POST' and 'delete' not in request.POST:
        if child:
            form = ChildProfileForm(request.POST, request.FILES, instance=child)
        else:
            form = ChildProfileForm(request.POST, request.FILES)

        if form.is_valid():
            updated_child = form.save(commit=False)
            updated_child.user = request.user
            updated_child.save()
            return redirect('users:profile')  # Redirect to the profile page

    context = {
        'form': form,
        'children': children,  # List of children for the user
        'child': child,  # The current child being edited or deleted
    }

    return render(request, 'profile_view.html', context)
def program_aktif(request):
    return render(request,'program_aktif.html')
def riwayat_kegiatan(request):
    return render(request,'riwayat_kegiatan.html')
def laporan_perkembangan(request):
    return render(request,'laporan_perkembangan.html')
def pembayaran(request):
    return render(request,'riwayat_pembayaran.html')