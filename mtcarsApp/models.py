from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Cliente(AbstractUser):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    email_confirmado = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='cliente_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='cliente_permissions',
        blank=True
    )
    
    def __str__(self):
        return f'{self.email}'

class Carro(models.Model):
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    disponibilidade = models.BooleanField(default=True)
    estoque = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    clientes_reservados = models.ManyToManyField(Cliente, related_name="carros_reservados", blank=True)
    clientes_interessados = models.ManyToManyField(Cliente, related_name="carros_interessados", blank=True)
    
    def __str__(self):
        return f'{self.modelo} {self.ano}'
    
    
'''
    a lambda function atualizaCarroDB
    já notifica por email quando o carro chegar
    para os assinantes_interessados

'''

    