from django.views.generic import TemplateView, RedirectView
from django.contrib import messages


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