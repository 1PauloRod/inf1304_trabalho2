# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Carro

# Dados dos carros a serem inseridos
carros_data = [
    {'modelo': 'Toyota Corolla', 'ano': 2024, 'disponibilidade': True, 'estoque': 12, 'preco': 130000},
    {'modelo': 'Honda Civic', 'ano': 2023, 'disponibilidade': True, 'estoque': 8, 'preco': 140000},
    {'modelo': 'Chevrolet Onix', 'ano': 2024, 'disponibilidade': True, 'estoque': 15, 'preco': 78000},
    {'modelo': 'Ford Ranger', 'ano': 2023, 'disponibilidade': True, 'estoque': 10, 'preco': 250000},
    {'modelo': 'Volkswagen Polo', 'ano': 2024, 'disponibilidade': True, 'estoque': 20, 'preco': 98000},
    {'modelo': 'Hyundai HB20', 'ano': 2023, 'disponibilidade': True, 'estoque': 18, 'preco': 75000},
    {'modelo': 'Jeep Compass', 'ano': 2024, 'disponibilidade': True, 'estoque': 6, 'preco': 190000},
    {'modelo': 'Nissan Kicks', 'ano': 2023, 'disponibilidade': True, 'estoque': 14, 'preco': 120000},
    {'modelo': 'Renault Duster', 'ano': 2024, 'disponibilidade': True, 'estoque': 10, 'preco': 115000},
    {'modelo': 'Fiat Argo', 'ano': 2024, 'disponibilidade': True, 'estoque': 22, 'preco': 72000},
    {'modelo': 'Chevrolet Tracker', 'ano': 2023, 'disponibilidade': True, 'estoque': 9, 'preco': 130000},
    {'modelo': 'Toyota Hilux', 'ano': 2024, 'disponibilidade': True, 'estoque': 7, 'preco': 290000},
    {'modelo': 'Volkswagen T-Cross', 'ano': 2023, 'disponibilidade': True, 'estoque': 11, 'preco': 135000},
    {'modelo': 'Peugeot 208', 'ano': 2024, 'disponibilidade': True, 'estoque': 16, 'preco': 95000},
    {'modelo': 'Ford Ka', 'ano': 2023, 'disponibilidade': True, 'estoque': 13, 'preco': 68000}
]

# Signal para povoar os dados após as migrações
@receiver(post_migrate)
def populate_carros(sender, **kwargs):
    for carro_data in carros_data:
        # Verifica se o carro já existe, caso contrário, cria um novo
        try:
            carro = Carro.objects.get(modelo=carro_data['modelo'], ano=carro_data['ano'])
        except ObjectDoesNotExist:
            Carro.objects.create(**carro_data)
