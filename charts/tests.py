from django.test import TestCase
from django.urls import reverse


class ViewsTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/sites/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('countries'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('tweet_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app/tweet_list.html')
