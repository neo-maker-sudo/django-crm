from django.test import TestCase
from django.urls import reverse


class LandingPageTest(TestCase):
    
    def test_landing_page(self):
        res = self.client.get(reverse("leads_landing"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "landing.html")
