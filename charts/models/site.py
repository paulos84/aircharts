from django.db import models
from django.urls import reverse
from charts.models.site_data import site_list, get_info


class LondonSiteManager(models.Manager):
    def london_sites(self):
        return self.filter(region='Greater London')


class SiteManager(models.QuerySet):
    def regions(self):
        return [a for a in self.values_list('region', flat=True).order_by('region').distinct()]

    def non_london_set1(self):
        return self.exclude(region='Greater London').filter(region__in=self.regions()[:11])

    def non_london_set2(self):
       return self.exclude(region='Greater London').filter(region__in=self.regions()[11:])


class Site(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Site name')
    code = models.CharField(unique=True, max_length=10, verbose_name='Site code')
    region = models.CharField(max_length=50, db_index=True)
    environment = models.CharField(max_length=50)
    url = models.URLField(max_length=1000, verbose_name='DEFRA website link', help_text='URL link to DEFRA webpage')
    map_url = models.URLField(max_length=1000, verbose_name='Google maps url')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    slug = models.CharField(unique=True, max_length=10)

    objects = SiteManager.as_manager()
    london_sites = LondonSiteManager()
    # uk_sites = UKSiteManager()

    class Meta:
        ordering = ('region',)

    def __repr__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('site_detail', kwargs={'slug': self.slug})

    @staticmethod
    def populate():
        """ create and save objects using the initial sites data """
        for site in site_list:
            site_entry = Site.objects.create(**get_info(site))
            site_entry.save()
