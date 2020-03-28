from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        """
        This test is redundant after adding
        test_home_page_returns_correct_html_with_test_client, that automatically
        tests url resolve.
        """
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        This is non-Djangoish version of the test, since it doesn't use
        TestCase.client
        """
        request = HttpRequest()
        response = home_page(request)  # instance of HttpResponse
        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_home_page_returns_correct_html_with_test_client(self):
        """ Use Django Test Client. Testing of html content = testing constants,
         which is wrong. Test whether the correct template was used, instead.
         We don't need to decode html content here.
         """
        response = self.client.get('/')

        # behold the magic power of Django's test client!
        self.assertTemplateUsed(response, 'index.html')
