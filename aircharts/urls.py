from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView

from charts.views import site_detail_view, site_list_view, map_view

urlpatterns = [
      path('admin/', admin.site.urls),
      re_path(r'^$', RedirectView.as_view(url='/sites/', permanent=True)),
      re_path(r'^map$', map_view.UKMapView.as_view(), name='map'),
      re_path(r'^sites/$', site_list_view.SiteListView.as_view(), name='sites'),
      path('sites/<slug>', site_detail_view.SiteDetailView.as_view(), name='site_detail'),
      path('sites/<site_code>/<int:days>', site_detail_view.SiteDetailDaysView.as_view(), name='site_detail_days'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

