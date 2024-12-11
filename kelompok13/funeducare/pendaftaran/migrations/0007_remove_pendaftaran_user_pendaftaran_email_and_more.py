# Generated by Django 5.1.3 on 2024-12-10 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pendaftaran', '0006_remove_pendaftaran_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendaftaran',
            name='user',
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Alamat Email'),
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='nama_ortu',
            field=models.CharField(max_length=100, null=True, verbose_name='Nama Orang Tua'),
        ),
        migrations.AlterField(
            model_name='pendaftaran',
            name='umur_anak',
            field=models.PositiveIntegerField(verbose_name='Umur Anak'),
        ),
    ]
