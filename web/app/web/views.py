from django.views.generic.base import TemplateView

class OpenAPIView(TemplateView):

    template_name = "web/openapi.yml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context