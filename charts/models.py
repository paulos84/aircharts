from django.db import models
from django.urls import reverse


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
