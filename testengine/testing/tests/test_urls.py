
from django.urls import reverse, resolve
from django.test import SimpleTestCase

from testing.views import index, QuestionsView
from testing.views import TestDetail as MyTestDetail


class TestUrls(SimpleTestCase):
    """ In this file django unit test has been used"""

    def test_tests_index(self):
        url = reverse('testing:tests_index')
        self.assertEqual(resolve(url).func, index)

    def test_questions_url(self):
        url = reverse('testing:questions_url')
        self.assertEqual(resolve(url).func.view_class, QuestionsView)

    def test_test_detail_url(self):
        url = reverse("testing:test_detail_url", args=['random-slug'])
        self.assertEqual(resolve(url).func.view_class, MyTestDetail)
