# Generated by Django 5.1.3 on 2024-12-09 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
