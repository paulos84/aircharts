from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
import charts.views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r'^$', RedirectView.as_view(url='/sites/', permanent=True)),
                  #re_path(r'^tweets/$', charts.views.TweetListView.as_view(), name='tweet_list'),
                  #re_path(r'^map$', charts.views.TweetMapView.as_view(), name='tweet_map'),
                  re_path(r'^sites/$', charts.views.SiteListView.as_view(), name='sites'),
                  #re_path(r'^countries/(?P<pk>\d+)$', charts.views.CountryDetailView.as_view(), name='country_detail'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)