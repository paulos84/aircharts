from django.views import generic
from .models import Site


class SiteListView(generic.ListView):
    model = Site
    #regions = set([a.region for a in Site.objects.all()])

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs) # get the default context data
        context['regions'] = set([a.region for a in Site.objects.all()])
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
