# -*- coding: utf-8 -*-
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView, ListView

from kid_bazaar.apps.payments.payments import create_submerchant

from . import models


class MessageRedirectionMixin(RedirectView):
    permanent = False
    message = None
    message_context = {}
    message_level = messages.INFO

    def get(self, request, *args, **kwargs):
        msg = kwargs.get('message') or self.message
        msg_level = kwargs.get('message_level') or self.message_level
        if msg is None:
            raise Exception("Message is not defined")

        msg = msg.format(**self.message_context)
        messages.add_message(request, msg_level, msg)

        return super(MessageRedirectionMixin, self).get(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = 'home/index.html'


class AddItemView(TemplateView):
    template_name = 'home/index.html'


class EditItemView(TemplateView):
    template_name = 'home/index.html'


class MyItemsView(ListView):
    template_name = 'items/mine.html'
    model = models.Item

    def get_queryset(self):
        my_kid = self.request.user.kid_set.first()
        if my_kid:
            return self.request.user.kid_set.first().item_set.all()
        return []


class SearchItemsView(ListView):
    template_name = 'items/search.html'
    model = models.Item

    def get_queryset(self):
        my_kid = self.request.user.kid_set.first()
        search_items = models.Item.objects.exclude(_is_paid=True)
        if my_kid:
            search_items = search_items.exclude(owner=my_kid)
        return search_items

class ProfileView(TemplateView):
    template_name = 'home/index.html'


class LogoutView(MessageRedirectionMixin):
    url = '/'
    message = 'Successfully logged out.'
    message_level = messages.INFO

    def get(self, request, *args, **kwargs):
        auth_views.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(MessageRedirectionMixin):
    message_level = messages.SUCCESS

    @property
    def url(self):
        return reverse('my_items')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user, created = auth.get_user_model().objects.get_or_create(email=email)
        if created:
            # we don't care about creation status web-hooks for now...
            user.merchant_id = create_submerchant(email)
            user.save()

        user = auth.authenticate(email=email)
        auth.login(request, user)
        if created:
            message = u'Thank you for registering!'
        else:
            message = u'Welcome back!'
        return super(RegisterView, self).get(request, *args, message=message)
