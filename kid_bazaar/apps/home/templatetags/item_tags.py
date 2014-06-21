from __future__ import unicode_literals, absolute_import

from django import template

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