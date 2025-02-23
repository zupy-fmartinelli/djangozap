# Generated by Django 5.0.12 on 2025-02-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0007_alter_whatsappinstance_qrcode_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsappinstance',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='whatsappinstance',
            name='phone_number',
            field=models.CharField(help_text='Número de telefone vinculado', max_length=20, unique=True),
        ),
    ]
