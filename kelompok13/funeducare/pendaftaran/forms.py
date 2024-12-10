from django import forms
from programs.models import Program, Fee

class BookingForm(forms.Form):
    nama_ortu = forms.CharField(
        label='Nama Orang Tua',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Isi nama orang tua',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Isi dengan email anda',
            }
        ),
        label="Alamat Email"
    )
    nomor_wa = forms.CharField(
        label='Nomor WhatsApp Orang Tua',
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Isi nomor whatsapp orang tua',
            }
        )
    )
    alamat = forms.CharField(
        label='Alamat Orang Tua',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Isi alamat rumah dari orang tua meliputi RT, RW, Desa, Kecamatan, Kabupaten',
            }
        )
    )
    ktp = forms.FileField(
        label="Upload KTP Orang Tua",
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*,application/pdf',
            }
        ),
        required=True,
    )
    nama_anak = forms.CharField(
        label='Nama Anak',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Isi nama lengkap anak',
            }
        )
    )
    umur_anak = forms.CharField(
        label='Umur Anak',
        max_length=2,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Isi umur anak',
            }
        )
    )
    jenis_kelamin = forms.ChoiceField(
        label='Jenis kelamin',
        widget=forms.RadioSelect(),
        choices=[
            ('L', 'Laki - laki'),
            ('P', 'Perempuan')
        ]
    )
    akta_kelahiran = forms.FileField(
        label="Upload Akta Kelahiran Anak",
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*,application/pdf',
            }
        ),
        required=True,
    )
    
    program = forms.ModelChoiceField(
        label='Program',
        queryset=Program.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'program-select'}),
        empty_label="Pilih Program"
    )
    
    fee = forms.ModelChoiceField(
        label='Jenis Program',
        queryset=Fee.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'fee-select'}),
        empty_label="Pilih Jenis Program"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'program' in self.data:
            try:
                program_id = int(self.data.get('program'))
                self.fields['fee'].queryset = Fee.objects.filter(program_id=program_id)
            except (ValueError, TypeError):
                pass
    
def clean_ktp(self):
    ktp = self.cleaned_data.get('ktp')
    if ktp:
        # Validasi ukuran file (maksimal 5MB)
        if ktp.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Ukuran file terlalu besar. Maksimal 5MB.")
        # Validasi tipe file
        valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
        ext = ktp.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError("Format file tidak didukung. Gunakan JPG, JPEG, PNG, atau PDF.")
    return ktp

def clean_akta_kelahiran(self):
    akta = self.cleaned_data.get('akta_kelahiran')
    if akta:
        # Validasi ukuran file (maksimal 5MB)
        if akta.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Ukuran file terlalu besar. Maksimal 5MB.")
        # Validasi tipe file
        valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
        ext = akta.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError("Format file tidak didukung. Gunakan JPG, JPEG, PNG, atau PDF.")
    return akta