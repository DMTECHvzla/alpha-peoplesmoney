"""
"""
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

# Create your models here.

SELECT_CATEGORY_CHOICES = [
    ("Comida", "Comida"),
    ("Transporte", "Transporte"),
    ("Compras", "Compras"),
    ("Servicios", "Servicios"),
    ("Entretenimiento", "Entretenimiento"),
    ("Otro", "Otro"),
]

ADD_OP_CHOICES = [
    ("Egreso", "Egreso"),
    ("Ingreso", "Ingreso"),
]

class Expense(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='something')
    type = models.CharField(max_length=10, choices=ADD_OP_CHOICES, default='Egreso')
    qty = models.IntegerField(default=0)
    date = models.DateField(default=now) 
    category = models.CharField(max_length=20, choices=SELECT_CATEGORY_CHOICES, default='Comida')
