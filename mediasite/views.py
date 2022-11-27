from django.views.generic.base import TemplateView
from articles.forms import SearchForm

class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm()
        context['form'] = form
        return context