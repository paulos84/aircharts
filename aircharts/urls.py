from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
import charts.views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r'^$', RedirectView.as_view(url='/sites/', permanent=True)),
                  #re_path(r'^map$', charts.views.TweetMapView.as_view(), name='map'),
                            # have the above map route link in sidebar
                  re_path(r'^sites/$', charts.views.SiteListView.as_view(), name='sites'),
                  re_path(r'^sites/(?P<pk>\d+)$', charts.views.SiteDetailView.as_view(), name='site_detail'),
                            #  have chart along with info in site_dict

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)