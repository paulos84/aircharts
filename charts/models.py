from django.db import models
from django.urls import reverse
from .site_data import site_list, get_info


class Site(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Site name')
    code = models.CharField(unique=True, max_length=10, verbose_name='Site code')
    region = models.CharField(max_length=50)
    environment = models.CharField(max_length=50)
    url = models.URLField(max_length=1000, verbose_name='DEFRA website link', help_text='URL link to DEFRA webpage')
    map_url = models.URLField(max_length=1000, verbose_name='Google maps url')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    slug = models.CharField(unique=True, max_length=10)

    class Meta:
        ordering = ('name',)

    def __repr__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('site_detail', kwargs={'slug': self.slug})

    @staticmethod
    def populate():
        """ create and save objects using the data in data.site_info.py """
        for site in site_list:
            site_entry = Site.objects.create(**get_info(site), slug=get_info(site)['code'])
            site_entry.save()
