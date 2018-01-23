from django.views import generic
from .models import Site


class SiteListView(generic.ListView):
    model = Site
    #queryset = Site.objects.order_by('region')

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        regions1 = Site.objects.values_list('region')[:8]
        regions2 = Site.objects.values_list('region')[8:]
        queryset1 = Site.objects.filter(region__in=regions1).order_by('region')
        queryset2 = Site.objects.filter(region__in=regions2).order_by('region')

        context = {
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
            'object_list': queryset1,
            'object_list3': queryset2
        }
        return context

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
