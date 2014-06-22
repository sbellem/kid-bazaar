from __future__ import unicode_literals, absolute_import

from django import template

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional


register = template.Library()


@tag(register, [Variable(), Variable(), Optional([Constant("as"), Name()])])
def navactive(context, request, urls, asvar=None):
    url_name = request.resolver_match.url_name
    if request.resolver_match.namespace:
        url_name = '%s:%s' % (request.resolver_match.namespace, url_name)
    output = "active " if url_name in urls.split() else ""
    if asvar:
        context[asvar] = output
        return ""
    else:
        return output
