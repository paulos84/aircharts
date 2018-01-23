from django.views import generic
from .models import Site


class SiteListView(generic.ListView):
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
