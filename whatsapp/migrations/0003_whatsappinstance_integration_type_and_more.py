# Generated by Django 5.0.12 on 2025-02-17 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0002_whatsappinstance_qrcode_url_whatsappinstance_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatsappinstance',
            name='integration_type',
            field=models.CharField(choices=[('WHATSAPP-BAILEYS', 'Baileys (Não Oficial)'), ('WHATSAPP-BUSINESS', 'WhatsApp Cloud API (Oficial)'), ('EVOLUTION', 'Evolution API')], default='WHATSAPP-BAILEYS', help_text='Tipo de integração com WhatsApp', max_length=20),
        ),
        migrations.AlterField(
            model_name='whatsappinstance',
            name='token',
            field=models.CharField(blank=True, help_text='Token da instância gerado pela API', max_length=255, null=True),
        ),
    ]
