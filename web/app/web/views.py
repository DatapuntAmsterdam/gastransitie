from django.views.generic.base import TemplateView

class OpenAPIView(TemplateView):

    template_name = "web/openapi.yml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        host = self.request.META['HTTP_HOST']
        if host.startswith('localhost'):
            context['apihost'] = 'http://' + host
            context['oauth2host'] = 'http://localhost:8686'
        else:
            context['apihost'] = 'https://' + host
            context['oauth2host'] = 'https://' + host
        return context