from django.views.generic import TemplateView
from apps.vacations.models import Vacation


# View for rendering the home page with a list of vacations.
class HomeView(TemplateView):
    template_name = 'core/home.html'

    # Get context data for the home page, including all vacations.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacations'] = Vacation.objects.all().order_by('-created_at')
        return context