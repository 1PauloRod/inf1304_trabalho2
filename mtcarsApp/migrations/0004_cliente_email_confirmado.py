# Generated by Django 5.1.3 on 2024-11-24 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtcarsApp', '0003_carro_clientes_interessados'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='email_confirmado',
            field=models.BooleanField(default=False),
        ),
    ]
