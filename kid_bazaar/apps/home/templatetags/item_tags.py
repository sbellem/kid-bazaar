# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django import template
from django.core.urlresolvers import reverse

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional


register = template.Library()

AGE_MONTH_THRESHOLD = 24


def age_text(age):
    if age < AGE_MONTH_THRESHOLD:
        return '%dm' % age
    else:
        return '%dyrs' % (age / 12)

register.filter('age_text', age_text)


@tag(register, [Variable(), Optional([Constant("as"), Name()])])
def kiditemactive(context, item, asvar=None):
    is_item_active = item.is_active()
    if is_item_active < 0:
        output = 'before'
    elif is_item_active > 0:
        output = 'after'
    else:
        output = 'now'

    if asvar:
        context[asvar] = output
        return ""
    else:
        return output


@register.simple_tag
def item_status(item, user_viewing):
    """When viewing my-items"""
    accepted = item.itemrequest_set.filter(status='ACCEPTED')
    if accepted.exists():
        if item.owner == user_viewing:
            return 'booked for {} [<a href="TODO">transfer</a>]'.format(accepted[0].requesting_user.email)
        else:
            return 'booked from {}'.format(accepted[0].owner.email)
    
    payment_pending = item.itemrequest_set.filter(status='PENDING_PAYMENT')
    if payment_pending.exists():
        if item.owner == user_viewing :
            return 'payment pending from {}'.format(payment_pending[0].requesting_user.email)
        else:
            return 'booking confirmed [<a href="{}">pay</a>]'.format(reverse('do_sale', kwargs={'item_id': item.id}))

    return ''
