from django.views import generic
import requests
import pytz
from datetime import datetime
from charts.models.site import Site
from charts.models.site_data import site_codes, site_geo2

local_tz = pytz.timezone('Europe/London')


class SiteDetailView(generic.DetailView):
    model = Site

    @staticmethod
    def get_data(site_code, days=2):
        data = requests.get('http://ukair.pauljd.me/site-data/{}/{}/'.format(site_code, days)).json()
        no2 = [float(i['no2']) if i['no2'].isdigit() else '' for i in data]
        pm25 = [float(i['pm25']) if i['pm25'].isdigit() else '' for i in data]
        pm10 = [float(i['pm10']) if i['pm10'].isdigit() else '' for i in data]
        hours = [i['time'][11:16] for i in data]
        return dict(no2=no2[::-1], pm25=pm25[::-1], pm10=pm10[::-1], times=hours[::-1])

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)  # get the default context data
        chart_data = self.get_data(self.kwargs['slug'])
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
