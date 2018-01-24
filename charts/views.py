from django.views import generic
from django.urls import reverse
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


class SiteDetailView(generic.DetailView):
    model = Site


"""
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
