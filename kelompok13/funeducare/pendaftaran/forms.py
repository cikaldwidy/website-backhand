from django import forms
from programs.models import Program, Fee
from users.models import Child

class BookingForm(forms.Form):
    # Field anak, hanya menampilkan anak-anak milik user yang login
    nama_anak = forms.ModelChoiceField(
        queryset=Child.objects.all(),  # Awalnya kosong
        label="Daftar Anak Anda", 
        empty_label="Pilih Anak",  
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'child-select'})
    )
    
    program = forms.ModelChoiceField(
        label='Program',
        queryset=Program.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'program-select'}),
        empty_label="Pilih Program"
    )
    
    fee = forms.ModelChoiceField(
        label='Jenis Program',
        queryset=Fee.objects.none(),  # Awalnya kosong
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'fee-select'}),
        empty_label="Pilih Jenis Program"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Ambil user yang sedang login
        super().__init__(*args, **kwargs)

        # Pastikan pilihan anak hanya untuk user yang login
        if user:
            self.fields['nama_anak'].queryset = Child.objects.filter(user=user)  # Filter anak berdasarkan user yang login
        
        # Update pilihan fee berdasarkan program yang dipilih
        if 'program' in self.data:
            try:
                program_id = int(self.data.get('program'))
                self.fields['fee'].queryset = Fee.objects.filter(program_id=program_id)
            except (ValueError, TypeError):
                pass

   
    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        program = self.cleaned_data.get('program')
        if fee and program:
            # Pastikan fee yang dipilih adalah bagian dari program yang dipilih
            if fee.program != program:
                raise forms.ValidationError("Jenis program tidak sesuai dengan program yang dipilih.")
        return fee

    # Validasi secara keseluruhan (opsional, bisa digunakan untuk pemeriksaan tambahan)
    def clean(self):
        cleaned_data = super().clean()
        # Pastikan program dan fee valid
        program = cleaned_data.get('program')
        fee = cleaned_data.get('fee')
        if not program:
            raise forms.ValidationError("Program harus dipilih.")
        if not fee:
            raise forms.ValidationError("Jenis program harus dipilih.")
        return cleaned_data
