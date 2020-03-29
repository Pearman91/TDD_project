from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.models import Item
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

    def test_can_save_post_request(self):
        response = self.client.post('/', data={'item_text': 'New list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New list item')

    def test_redirects_after_post(self):
        response = self.client.post('/', data={'item_text': 'New list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_show_all_list_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/')

        self.assertIn('item1', response.content.decode())
        self.assertIn('item2', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first bloody item in da list'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item in the list'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,
                         'The first bloody item in da list')
        self.assertEqual(second_saved_item.text, 'The second item in the list')

    def test_only_saves_items_on_post(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

