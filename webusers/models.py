from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import UserManager
from django.utils.translation import ugettext_lazy as _
from localflavor.br.models import BRCPFField, BRCNPJField, BRPostalCodeField, BRStateField
# Create your models here.
'''

class Address(models.Model):
    country = models.CharField(_("País"), blank=True, null=True,  max_length=254)
    state = models.CharField(_("Estado"), blank=True, null=True,  max_length=254)
    city = models.CharField(_("Município"), blank=True, null=True,  max_length=254)
    zipcode = BRPostalCodeField(_("CEP"), blank=True, max_length=254, null=True)
    street = models.CharField(_("Rua"), blank=True, null=True, max_length=10000)
    number = models.IntegerField(_("Número"), blank=True, null=True)
    reference = models.CharField(_("Complemento"),  blank=True, null=True, max_length=10000)
'''
class User(AbstractBaseUser):
    objects =  UserManager()
    name = models.CharField(_("Nome"), max_length=254)
    identity = BRCPFField(_("CPF"))
    email = models.EmailField(max_length=254, unique=True)
    pis = models.CharField(_("PIS"), blank=True, default='', max_length=254)
    country = models.CharField(_("País"), blank=True, default='', max_length=254)
    state = models.CharField(_("Estado"), blank=True, default='',  max_length=254)
    city = models.CharField(_("Município"), blank=True, default='',  max_length=254)
    zipcode = BRPostalCodeField(_("CEP"), blank=True, max_length=254, null=True)
    street = models.CharField(_("Rua"), blank=True, default='', max_length=10000)
    number = models.IntegerField(_("Número"))
    reference = models.CharField(_("Complemento"), blank=True, default='', max_length=10000)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
