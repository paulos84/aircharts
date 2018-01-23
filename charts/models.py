from django.db import models
from .site_data import site_list, get_info, regions, environs


class Site(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Site name')
    code = models.CharField(unique=True, max_length=10, verbose_name='Site code')
    url = models.URLField(max_length=1000, verbose_name='DEFRA website link', help_text='URL link to DEFRA webpage')
    map_url = models.URLField(max_length=1000, verbose_name='Google maps url')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    @property
    def region(self):
        hyphenated = regions.get(self.name)
        split_name = hyphenated.replace('-', ' ').split()
        self.formatted = ' '.join([a.capitalize() for a in split_name])
        return self.formatted

    @property
    def environment(self):
        hyphenated = environs.get(self.name)
        split_name = hyphenated.replace('-', ' ').split()
        self.formatted = ' '.join([a.capitalize() for a in split_name])
        return self.formatted

    class Meta:
        ordering = ('name',)

    def __repr__(self):
        return self.name

    @staticmethod
    def populate():
        """ create and save objects using the data in data.site_info.py """
        for site in site_list:
            site_entry = Site.objects.create(**get_info(site))
            site_entry.save()
