from django.views import generic
import requests
import pytz
from datetime import datetime
from .models import Site
from .site_data import site_codes, site_names, site_geo2, locations

local_tz = pytz.timezone('Europe/London')


def latest_hour_max():
    data = requests.get('http://ukair.pauljd.me/current-data/').json()
    p_max = max(float(a['pm10']) if a['pm10'].isdigit() else 0 for a in data)
    p_codes = [i['site_code'] for i in data if i['pm10'] == str(round(p_max))]
    n_max = max(float(a['no2']) if a['no2'].isdigit() else 0 for a in data)
    n_codes = [i['site_code'] for i in data if i['no2'] == str(round(n_max))]
    return {'pm10_max': p_max, 'pm10_sites': p_codes, 'no2_max': n_max, 'no2_sites': n_codes}


class SiteListView(generic.ListView):
    model = Site

    def get_context_data(self, **kwargs):
        region_set = Site.objects.values_list('region').order_by('region').distinct()
        regions = [a[0] for a in region_set]
        qs_london = Site.objects.filter(region='Greater London')
        queryset1 = Site.objects.filter(region__in=regions[:11]).exclude(region='Greater London').order_by('region')
        queryset2 = Site.objects.filter(region__in=regions[11:]).order_by('region')
        context = {'object_list_lon': qs_london,
                   'object_list': queryset1,
                   'object_list2': queryset2,
                   'date': datetime.now(local_tz),
                   'site_names': site_names,
                   **latest_hour_max()}
        return context


def get_data(site_code, days=4):
    data = requests.get('http://ukair.pauljd.me/site-data/{}/{}/'.format(site_code, days)).json()
    no2 = [float(i['no2']) if i['no2'].isdigit() else '' for i in data]
    pm25 = [float(i['pm25']) if i['pm25'].isdigit() else '' for i in data]
    pm10 = [float(i['pm10']) if i['pm10'].isdigit() else '' for i in data]
    hours = [i['time'][11:16] for i in data]
    return dict(no2=no2[::-1], pm25=pm25[::-1], pm10=pm10[::-1], times=hours[::-1])


class SiteDetailView(generic.DetailView):
    model = Site

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)  # get the default context data
        chart_data = get_data(self.kwargs['slug'])
        context['chartID'] = 'chart_ID'
        context['chart'] = {"renderTo": 'chart_ID', "type": 'line', "height": 522.5, "width": 784}
        context['series'] = [{"name": 'PM10', "data": chart_data['pm10']},
                             {"name": 'PM2.5', "data": chart_data['pm25']},
                             {"name": 'Nitrogen Dioxide', "data": chart_data['no2']}]
        site_names = {b: a for a, b in site_codes.items()}
        site_name = site_names.get(self.kwargs['slug'])
        context['title'] = {"text": 'Recent air pollution levels for {}'.format(site_name)}
        context['xAxis'] = {"categories": chart_data['times']}
        context['yAxis'] = {"title": {"text": 'Concentration (ug/m3)'}}
        context['location'] = [[site_name, site_geo2.get(site_name)[0], site_geo2.get(site_name)[1]]]
        context['lat'] = site_geo2.get(site_name)[0]
        context['long'] = site_geo2.get(site_name)[1]
        context['date'] = datetime.now(local_tz)
        return context


class UKMapView(generic.ListView):
    model = Site
    template_name = 'charts/uk_map.html'

    def get_context_data(self, **kwargs):
        context = super(UKMapView, self).get_context_data(**kwargs)
        context['locations'] = locations
        return context
