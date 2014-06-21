# -*- coding: utf-8 -*-
import decimal
from datetime import date
from dateutil.relativedelta import relativedelta

from cloudinary.models import CloudinaryField
from custom_user.models import AbstractEmailUser
from django.conf import settings
from django.db import models

from kid_bazaar.apps.payments.payments import get_payments_list


class Kid(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.TextField(blank=True)
    birthday = models.DateField(blank=True)
    pic = CloudinaryField('image', blank=True, null=True)
    sex = models.TextField(blank=True)

    def age(self):
        age = relativedelta(date.today(), self.birthday)
        return 12 * age.years + age.months

    def __unicode__(self):
        return u'{} of {}'.format(self.name, self.parent)


class Item(models.Model):
    owner = models.ForeignKey(Kid)
    pic = CloudinaryField('image', blank=True, null=True)
    name = models.TextField()
    description = models.TextField(blank=True)
    category = models.TextField(blank=True)
    age_from = models.IntegerField()  # in months
    age_to = models.IntegerField()  # in months
    price = models.DecimalField(null=True, decimal_places=2, max_digits=7)

    _is_paid = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{} of {}'.format(self.name, self.owner.parent)

    @property
    def is_paid(self):
        if not self.price:
            return False
        # _is_paid holds a "cached" status if item has been paid in order to avoid always querying braintree's API
        if not self._is_paid:
            self.update_is_paid()
        return self._is_paid

    def update_is_paid(self):
        # we don't care about payment status for now and we check all payments made...
        payments_list = get_payments_list(self.id)
        payments_amount = sum([p.amount for p in payments_list.items])
        self._is_paid = decimal.Decimal(payments_amount) > self.price
        self.save()


class ItemRequest(models.Model):
    item = models.ForeignKey(Item)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items_sold')
    requesting_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items_wanted')
    status = models.TextField(default='PENDING')  # can be PENDING/ACCEPTED/REJECTED


class KBUser(AbstractEmailUser):
    merchant_id = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'{} [merchant_id={}]'.format(self.email, self.merchant_id)
