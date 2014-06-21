# -*- coding: utf-8 -*-
from cloudinary.models import CloudinaryField
from custom_user.models import AbstractEmailUser
from django.conf import settings
from django.db import models


class Kid(models.Model):
    parent = models.IntegerField(settings.AUTH_USER_MODEL)
    name = models.TextField(blank=True)
    birthday = models.DateField(blank=True)
    pic = CloudinaryField('image')
    sex = models.TextField(blank=True)


class Item(models.Model):
    owner = models.ForeignKey(Kid)
    pic = CloudinaryField('image')
    name = models.TextField()
    description = models.TextField(blank=True)
    category = models.TextField(blank=True)
    age_from = models.IntegerField()  # in months
    age_to = models.IntegerField()  # in months
    used_till = models.DateField()  # automatically calculated, when item is passed
    price = models.DecimalField(null=True, decimal_places=2, max_digits=7)


class ItemRequest(models.Model):
    item = models.ForeignKey(Item)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items_sold')
    requesting_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items_wanted')
    status = models.TextField(default='PENDING')  # can be PENDING/ACCEPTED/REJECTED


class KBUser(AbstractEmailUser):
    merchant_id = models.TextField(null=True, blank=True)
