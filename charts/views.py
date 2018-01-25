from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
import requests
from .models import Site


class SiteListView(generic.ListView):
    model = Site
    #queryset = Site.objects.order_by('region')

    def get_context_data(self, **kwargs):
        region_set = Site.objects.values_list('region').order_by('region').distinct()
        regions = [a[0] for a in region_set]
        queryset1 = Site.objects.filter(region__in=regions[:11]).order_by('region')
        queryset2 = Site.objects.filter(region__in=regions[11:]).order_by('region')
        context = {'object_list': queryset1,
                   'object_list2': queryset2}
        return context


def get_data(site_code, days=5):
    data = requests.get('http://aurn-api.pauljd.me/site-data/{}/{}/'.format(site_code, days)).json()
    no2 = [float(i['no2']) if i['no2'].isdigit() else '' for i in data]
    pm25 = [float(i['pm25']) if i['pm25'].isdigit() else '' for i in data]
    pm10 = [float(i['pm10']) if i['pm10'].isdigit() else '' for i in data]
    times = [i['time'].split(' ')[1] for i in data]
    return dict(no2=no2, pm25=pm25, pm10=pm10, times=times)


class SiteDetailView(generic.DetailView):
    model = Site

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs) # get the default context data
        chart_data = get_data(self.kwargs['slug'])
        context['chartID'] = 'chart_ID'
        context['chart'] = {"renderTo": 'chart_ID', "type": 'line', "height": 550, "width": 800}
        context['series'] = [{"name": 'PM10', "data": chart_data['pm10']},
                             {"name": 'PM2.5', "data": chart_data['pm25']},
                             {"name": 'Nitrogen Dioxide', "data": chart_data['no2']}]
        context['title'] = {"text": 'Recent air pollution levels'}
        context['xAxis'] = {"categories": chart_data['times']}
        context['yAxis'] = {"title": {"text": 'Concentration (ug/m3)'}}
        return context


"""

def SiteDetailView(request, album_id):
    #album_id variable defined in the musics/urls.py urlpattern
    #where you use parametized url mapping (specify in urls.py - you must pass this in the view)
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album':album})

class TweetMapView(generic.ListView):
    model = Country
    template_name = 'app/tweet_map.html'

    def get_queryset(self):
        tweeted_about = Country.objects.filter(tweet__isnull=False)
        return tweeted_about


class CountryDetailView(generic.DetailView):
    model = Country


class TweetListView(generic.ListView):
    model = Tweet
    template_name = 'app/tweet_list.html'

    def get_queryset(self):
        tweets = Tweet.objects.all()[:50]
        return tweets

"""
