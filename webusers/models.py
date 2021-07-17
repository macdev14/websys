from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
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


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Favor inserir E-mail. ')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        return self._create_user(email, password, **extra_fields)



class User(AbstractBaseUser):
    objects =  CustomUserManager()
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
