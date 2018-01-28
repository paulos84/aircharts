from django.test import TestCase
from django.urls import reverse
from charts.models import Site


class ViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Site.objects.create(code='ABD', environment='Urban Background', latitude='57.157360', longitude='-2.094278',
                            map_url='https://maps.google.co.uk/?q=57.157360,-2.094278', name='Aberdeen',
                            region='North East Scotland', slug='ABD',
                            url='https://uk-air.defra.gov.uk/networks/site-info?site_id=ABD')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/sites/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('sites'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('sites'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'charts/site_list.html')

    def test_ukmap_view_context_data(self):
        resp = self.client.get('/map')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(['Aberdeen', 57.15736, -2.094278] in resp.context['locations'])

    def test_sitedetailview_context_data(self):
        abd = Site.objects.get(name='Aberdeen')
        resp = self.client.get(reverse('site_detail', kwargs={'slug': abd.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['chartID'], 'chart_ID')
        self.assertEqual(resp.context['location'], [['Aberdeen', 57.15736, -2.094278]])
        self.assertEqual(resp.context['title'] == 'Recent air pollution levels for Aberdeen')


class SiteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
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