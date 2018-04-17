from django.test import TestCase
from django.urls import reverse
from charts.models.site import Site


class ViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
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
