# Generated by Django 5.1.3 on 2024-12-10 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pendaftaran', '0008_alter_pendaftaran_nama_ortu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendaftaran',
            name='nama_ortu',
            field=models.CharField(max_length=100, null=True, verbose_name='Nama Orang Tua'),
        ),
    ]