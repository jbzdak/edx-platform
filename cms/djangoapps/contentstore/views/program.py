from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from openedx.core.djangoapps.programs.models import ProgramsApiConfig


class ProgramAuthoringView(TemplateView):
    """View rendering a template which plays host to the Programs authoring app."""
    template_name = 'program_authoring.html'

    def get_context_data(self, **kwargs):
        """Populate the context with values from configuration."""
        context = super(ProgramAuthoringView, self).get_context_data(**kwargs)

        programs_config = ProgramsApiConfig.current()
        context['authoring_app_config'] = programs_config.authoring_app_config
        context['programs_api_url'] = programs_config.public_api_url
        context['studio_home_url'] = reverse('home')

        return context
