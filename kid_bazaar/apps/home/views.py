# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.core.mail import EmailMessage, send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, RedirectView, ListView

from kid_bazaar.apps.payments.payments import create_submerchant
from . import forms, models


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

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return HttpResponseRedirect(reverse('my_items'))
        return super(IndexView, self).get(request, *args, **kwargs)


class AddItemView(MessageRedirectionMixin):
    template_name = 'home/add_item.html'
    message = u'Item has been added'
    message_level = messages.SUCCESS

    @property
    def url(self):
        return reverse('my_items')

    def get(self, request, *args, **kwargs):
        form = forms.ItemForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.ItemForm(data=request.POST)
        if not form.is_valid():
            render(request, self.template_name, {'form': form})
        data = dict(form.clean(), owner = request.user.kid_set.first())
        data['age_from'] = (data['age_from'] or 0) + (data.pop('age_from_years') or 0) * 12
        data['age_to'] = (data['age_to'] or 0) + (data.pop('age_to_years') or 0) * 12
        models.Item.objects.create(**data)
        return super(AddItemView, self).get(request, *args, **kwargs)


class EditItemView(TemplateView):
    template_name = 'home/edit_item.html'
    message = u'Item has been saved'
    message_level = messages.SUCCESS

    @property
    def url(self):
        return reverse('my_items')

    def get(self, request, item_id, *args, **kwargs):
        item = get_object_or_404(models.Item, id=item_id, owner=request.user.kid_set.first())
        form = forms.ItemForm(instance=item)
        return render(request, self.template_name, {'form': form})

    def post(self, request, item_id, *args, **kwargs):
        item = get_object_or_404(models.Item, id=item_id, owner=request.user.kid_set.first())
        form = forms.ItemForm(data=request.POST, instance=item)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        form.save()
        return HttpResponseRedirect(reverse('my_items'))


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
        item_ids = list(models.ItemRequest.objects.filter(
            status__in=['PENDING_PAYMENT', 'ACCEPTED']).values_list('item__id', flat=True))

        my_kid = self.request.user.kid_set.first()
        if my_kid:
            item_ids.extend(models.Item.objects.filter(owner=my_kid).values_list('id', flat=True))
        
        items = models.Item.objects.filter(id__in=set(item_ids))
        return sorted(items, key=lambda i: (-i.is_active(), i.age_from))


class SearchItemsView(ListView):
    template_name = 'items/search.html'
    model = models.Item

    def get_context_data(self, **kwargs):
        context = super(SearchItemsView, self).get_context_data(**kwargs)
        context.update({'q': self.request.GET.get('q', '')})
        return context

    @property
    def _base_qs(self):
        base_qs = models.Item.objects

        # exclude booked or in process of booking (by anyone) items
        not_free_items_ids = models.ItemRequest.objects.exclude(
            status__in=("PENDING_PAYMENT", "ACCEPTED")).values_list('id', flat=True)  
        base_qs = base_qs.exclude(id__in=not_free_items_ids)

        my_kid = self.request.user.kid_set.first()
        if my_kid:
            # exclude owned (by this user) items        
            base_qs = base_qs.exclude(owner=my_kid)

            # exclude stuff for younger kids (than this user's)
            base_qs = base_qs.filter(age_to__gte=my_kid.age())

        return base_qs

    def get_queryset(self):
        search_qs = self._base_qs

        q = self.request.GET.get('q')
        if q:
            search_qs = search_qs.filter(Q(name__icontains=q) | Q(category__icontains=q))

        return search_qs.order_by('age_from',)


class AddKidView(MessageRedirectionMixin):
    template_name = 'home/add_kid.html'
    message = u'Kid has been added'
    message_level = messages.SUCCESS

    @property
    def url(self):
        return reverse('my_items')

    def get(self, request, *args, **kwargs):
        form = forms.KidForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.KidForm(data=request.POST)
        if not form.is_valid():
            render(request, self.template_name, {'form': form})
        data = dict(form.clean(), parent = request.user)
        models.Kid.objects.create(**data)
        return super(AddKidView, self).get(request, *args, **kwargs)


class EditKidView(MessageRedirectionMixin):
    template_name = 'home/add_kid.html'
    message = u'Kid has been changed'
    message_level = messages.SUCCESS

    @property
    def url(self):
        return reverse('my_items')

    def get(self, request, item_id, *args, **kwargs):
        kid = get_object_or_404(models.Kid, id=item_id)
        form = forms.KidForm(instance=kid)
        return render(request, self.template_name, {'form': form})

    def post(self, request, item_id, *args, **kwargs):
        kid = get_object_or_404(models.Kid, id=item_id)
        form = forms.KidForm(data=request.POST, instance=kid)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        form.save()
        return HttpResponseRedirect(reverse('my_items'))


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
            message = u'Welcome back {}!'.format(user.email)
        return super(RegisterView, self).get(request, *args, message=message)


class BookingRequestView(MessageRedirectionMixin):
    message_level = messages.SUCCESS
    message = 'Owner has received an email with your booking request'

    @property
    def url(self):
        return reverse("search_items")

    # TODO change to POST
    def get(self, request, item_id, *args, **kwargs):
        item = get_object_or_404(models.Item, id=item_id)
        user = request.user
        item_owner_parent = item.owner.parent
        item_request = models.ItemRequest.objects.create(item=item, owner=item_owner_parent, requesting_user=user)
        confirmation_url = reverse('confirm_booking', kwargs={'item_request_id': item_request.id})
        body = 'Please click the <a href="{}{}">link</a> to accept the booking from {} for item {}'
        msg = EmailMessage(
            '[KID BAZAAR] Booking confirmation request',
            body.format(settings.HOST, confirmation_url, user.email, item.name),
            'noreply@kidbazaar.eu',
            [item_owner_parent.email]
        )
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
        return super(BookingRequestView, self).get(request, *args)


class ConfirmBookingView(MessageRedirectionMixin):
    message_level = messages.SUCCESS
    message = 'The booking request has been confirmed'

    def get(self, request, item_request_id, *args, **kwargs):
        item_request = get_object_or_404(models.ItemRequest, id=item_request_id)
        item = item_request.item
        if item.price > 0:
            item_request.status = 'PENDING_PAYMENT'
        else:
            item_request.status = 'ACCEPTED'
        item_request.save()

        body = 'Your booking request for item {} has been accepted!'
        send_mail(
            '[KID BAZAAR] Booking confirmation accepted',
            body.format(item.name),
            'noreply@kidbazaar.eu',
            [item_request.requesting_user.email],
            fail_silently=False
        )
        return HttpResponseRedirect('home')


class TransferView(MessageRedirectionMixin):
    message_level = messages.SUCCESS
    message = 'The booking request has been confirmed'

    def get(self, request, item_id, *args, **kwargs):
        if not request.user or not request.user.is_authenticated():
            return HttpResponseRedirect('/')

        item = get_object_or_404(models.Item, id=item_id, owner__parent=request.user)
        accepted = item.itemrequest_set.filter(status='ACCEPTED', owner=request.user)
        if accepted.exists():
            item.owner = accepted[0].requesting_user.kid_set.first()
            for ir in item.itemrequest_set.all():
                ir.delete()
            item.save()

        return HttpResponseRedirect('/')

