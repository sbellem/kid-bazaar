from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView, View


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


class MyItemsView(TemplateView):
    template_name = 'home/index.html'


class SearchItemsView(TemplateView):
    template_name = 'home/index.html'


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
        user = auth.authenticate(email=email)
        auth.login(request, user)
        if created:
            message = u'Thank you for registering!'
        else:
            message = u'Welcome back!'
        return super(RegisterView, self).get(request, *args, message=message)
