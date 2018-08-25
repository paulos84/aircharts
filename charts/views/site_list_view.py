from django.views import generic
import requests
import pytz
from datetime import datetime
from charts.models.site import Site
from charts.models.site_data import site_names

local_tz = pytz.timezone('Europe/London')


class SiteListView(generic.ListView):
    model = Site

    @staticmethod
    def latest_hour_max():
        data = requests.get('http://142.93.248.45/data/current').json()
        p_max = max(float(a['pm10']) if a['pm10'].isdigit() else 0 for a in data)
        p_codes = [i['site_code'] for i in data if i['pm10'] == str(round(p_max))]
        n_max = max(float(a['no2']) if a['no2'].isdigit() else 0 for a in data)
        n_codes = [i['site_code'] for i in data if i['no2'] == str(round(n_max))]
        return {'pm10_max': p_max, 'pm10_sites': p_codes, 'no2_max': n_max, 'no2_sites': n_codes}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_list_lon': Site.london_sites.all(),
            'object_list': Site.objects.non_london_set1,
            'object_list2': Site.objects.non_london_set2,
            'date': datetime.now(local_tz),
            'site_names': site_names,
            **self.latest_hour_max(),
        })
        return context
