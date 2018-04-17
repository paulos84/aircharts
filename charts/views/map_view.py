from django.views import generic
from charts.models.site import Site
from charts.models.site_data import locations


class UKMapView(generic.ListView):
    model = Site
    template_name = 'charts/uk_map.html'

    def get_context_data(self, **kwargs):
        context = super(UKMapView, self).get_context_data(**kwargs)
        context['locations'] = locations
        return context
