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


@tag(register, [Variable(), Optional([Variable(), Constant("as"), Name()])])
def kiditemactive(context, item, kid=None, asvar=None):
    is_item_active = item.is_active(kid)
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


@tag(register, [Variable(), Variable(), Optional([Constant("as"), Name()])])
def item_status(context, item, user_viewing, asvar=None):
    """When viewing my-items"""
    owner_user = item.owner.parent
    output = ''
    itemrequest = item.get_oldest_status_itemrequest()
    if not itemrequest:
        pass
    elif itemrequest.status == 'ACCEPTED':
        if owner_user == user_viewing:
            output = '<span class="label">booked</span><br/> for&nbsp;{} <br/>' \
                     '<a href="{}" class="btn btn-default btn-sm" role="button">transfer</a>' \
                     ''.format(itemrequest.requesting_user.email,
                               reverse('transfer_item', kwargs={'item_id': item.id}))
        else:
            output = '<span class="label">booked</span><br/> from {}'.format(itemrequest.owner.email)
    elif itemrequest.status == 'PENDING_PAYMENT':
        if owner_user == user_viewing:
            output = '<span class="label">payment pending</span><br/> from&nbsp;{}'.format(itemrequest.requesting_user.email)
        else:
            output = '<span class="label">booking confirmed</span><br/>' \
                     '<a href="{}/" class="btn btn-default btn-sm" role="button"' \
                     'style="margin-top: 5px;">pay</a>' \
                     ''.format(reverse('do_sale', kwargs={'item_id': item.id}))
    elif itemrequest.status == 'PENDING_CONFIRMATION':
        itemreqs = item.get_itemrequests('PENDING_CONFIRMATION')
        output = '<div class="dropdown">' \
                 '<span class="label" data-toggle="dropdown">pending requests <span class="caret"></span> </span> ' \
                 '<ul class="dropdown-menu text-left">' \
                 '{}' \
                 '</ul>' \
                 '</div>' \
                 ''.format(''.join(['<li><a href="{}">book for {}</a></li>'
                                    ''.format(reverse('confirm_booking', kwargs={'item_request_id': i.id}),
                                              i.requesting_user.email)
                                    for i in itemreqs])
        )
    if asvar:
        context[asvar] = output
        return ""
    else:
        return output


@tag(register, [Variable(), Variable(), Optional([Constant("as"), Name()])])
def kidowned(context, kid, item, asvar=None):
    if kid and kid.id == item.owner.id:
        output = 'owned'
    else:
        output = 'not-owned'

    if asvar:
        context[asvar] = output
        return ""
    else:
        return output


@tag(register, [Variable(), Variable(), Optional([Constant("as"), Name()])])
def item_has_been_requested(context, user, item, asvar=None):
    if item.has_requested_item(user):
        output = 'requested'
    else:
        output = ''

    if asvar:
        context[asvar] = output
        return ""
    else:
        return output
