from django.db import models
from .site_data import site_list, get_info, regions, format_label


class Region(models.Model):
    reg_name = models.CharField(unique=True, max_length=100, verbose_name='Site name')

    @staticmethod
    def populate():
        """ create and save objects using the data in the regions dictionary in site_data.py """
        for region in set(regions.values()):
            entry = Region.objects.create(reg_name=format_label(region))
            entry.save()


class Site(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Site name')
    region = models.ForeignKey(Region, on_delete='CASCADE')
    code = models.CharField(unique=True, max_length=10, verbose_name='Site code')
    environment = models.CharField(max_length=50)
    url = models.URLField(max_length=1000, verbose_name='DEFRA website link', help_text='URL link to DEFRA webpage')
    map_url = models.URLField(max_length=1000, verbose_name='Google maps url')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __repr__(self):
        return self.name

    @staticmethod
    def populate():
        """ create and save objects using the data in data.site_info.py """
        for site in site_list:
            site_dict = get_info(site)
            region_name = site_dict['region']
            region = Region.objects.get(reg_name=format_label(region_name))
            del site_dict['region']
            site_entry = Site.objects.create(**site_dict, region=region)
            site_entry.save()
