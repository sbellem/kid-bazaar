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
    birthday = models.DateField(blank=True, null=True)
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
        
        if self._is_paid:
            for ir in self.itemrequest_set.filter(status='PENDING_PAYMENT'):
                ir.status = 'ACCEPTED'
                ir.save()

    def is_active(self, kid=None):
        if not kid:
            kid = self.owner
        kids_age = kid.age()
        item_age_from = self.age_from
        item_age_to = self.age_to

        if kids_age < item_age_from:
            return -1
        elif kids_age <= item_age_to:
            return 0
        else:
            return 1

    def status(self):
        oldest_status = self.get_oldest_status_itemrequest()
        if oldest_status:
            return oldest_status.status
        else:
            return 'FREE'

    def accepted_itemrequest(self):
        output = [ir for ir in self.itemrequest_set.all() if ir.status == 'ACCEPTED']
        if output:
            return output[0]
        return None

    def booked_from(self):
        itemrequest = self.accepted_itemrequest()
        if itemrequest:
            return itemrequest.owner

    def booked_for(self):
        itemrequest = self.accepted_itemrequest()
        if itemrequest:
            return itemrequest.requesting_user

    def get_oldest_status_itemrequest(self):
        accepted = [i for i in self.itemrequest_set.all() if i.status == 'ACCEPTED']
        if accepted:
            return accepted[0]
        pending_payments = [i for i in self.itemrequest_set.all() if i.status == 'PENDING_PAYMENT']
        if pending_payments:
            return pending_payments[0]
        pending_confirmation = [i for i in self.itemrequest_set.all() if i.status == 'PENDING_CONFIRMATION']
        if pending_confirmation:
            return pending_confirmation[0]

    def get_itemrequests(self, status):
        return [i for i in self.itemrequest_set.all() if i.status == status]


class ItemRequest(models.Model):
    item = models.ForeignKey(Item)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items_sold')
    requesting_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items_wanted')
    # can be PENDING_CONFIRMATION -> PENDING_PAYMENT (if price > 0) -> ACCEPTED
    status = models.TextField(default='PENDING_CONFIRMATION')


class KBUser(AbstractEmailUser):
    merchant_id = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'{} [merchant_id={}]'.format(self.email, self.merchant_id)
