from django.test import TestCase
from charts.models.site import Site


class SiteModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up non-modified objects used by all test methods
        Site.objects.create(code='ABD', environment='Urban Background', latitude='57.157360', longitude='-2.094278',
                            map_url='https://maps.google.co.uk/?q=57.157360,-2.094278', name='Aberdeen',
                            region='North East Scotland', slug='ABD',
                            url='https://uk-air.defra.gov.uk/networks/site-info?site_id=ABD')

    def test_site_name_label(self):
        site = Site.objects.get(id=1)
        field_label = site._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Site name')

    def test_site_code_label(self):
        site = Site.objects.get(id=1)
        field_label = site._meta.get_field('code').verbose_name
        self.assertEquals(field_label, 'Site code')

    def test_map_url_max_length(self):
        site = Site.objects.get(id=1)
        max_length = site._meta.get_field('map_url').max_length
        self.assertEquals(max_length,1000)

    def test_get_absolute_url(self):
        site=Site.objects.get(id=1)
        self.assertEquals(site.get_absolute_url(), '/sites/ABD')
