# -*- coding: utf-8 -*-
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.db.models import Q
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
    my_kid = None

    def get_context_data(self, **kwargs):
        context = super(MyItemsView, self).get_context_data(**kwargs)
        context.update({'my_kid': self.my_kid})
        return context

    def get(self, request, *args, **kwargs):
        self.my_kid = self.request.user.kid_set.first()
        return super(MyItemsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.my_kid:
            items = self.my_kid.item_set.all()
            return sorted(items, key=lambda i: (-i.is_active(), i.age_from))
        return []


class SearchItemsView(ListView):
    template_name = 'items/search.html'
    model = models.Item

    @property
    def _base_qs(self):
        base_qs = models.Item.objects
        # exclude paid (by anyone) items
        base_qs = base_qs.exclude(_is_paid=True)
        # exclude owned (by this user) items        
        my_kid = self.request.user.kid_set.first()
        if my_kid:
            base_qs = base_qs.exclude(owner=my_kid)
        # exclude booked (by anyone) items
        not_free_items_ids = models.ItemRequest.objects.exclude(status="PENDING_CONFIRMATION").values('id',)   
        base_qs = base_qs.exclude(id__in=not_free_items_ids)
        return base_qs

    def get_queryset(self):
        search_qs = self._base_qs
        
        q = self.request.GET.get('q')
        if q:
            search_qs = search_qs.filter(Q(name__icontains=q) | Q(category__icontains=q))
         
        return search_qs



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
