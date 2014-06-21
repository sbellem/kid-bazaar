from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, RedirectView, View


class MessageRedirectionMixin(RedirectView):
    permanent = False
    message = None
    message_context = {}
    message_level = messages.INFO

    def get(self, request, *args, **kwargs):
        msg = self.message
        if msg is None:
            raise Exception("Message is not defined")

        msg = msg.format(**self.message_context)
        messages.add_message(request, self.message_level, msg)

        return super(MessageRedirectionMixin, self).get(request, *args, **kwargs)


# class RegistrationCompleteView(MessageRedirectionMixin):
#     url = '/'  # You can use pattern_name or get_redirect_url() instead see @RedirectView
#     message = 'Message'
#     message_level = messages.SUCCESS


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
