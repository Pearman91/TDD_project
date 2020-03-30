from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html_with_test_client(self):
        """ Use Django Test Client. Testing of html content = testing constants,
         which is wrong. Test whether the correct template was used, instead.
         We don't need to decode html content here.
         """
        response = self.client.get('/')

        # behold the magic power of Django's test client!
        self.assertTemplateUsed(response, 'index.html')


class ListViewTest(TestCase):

    def test_list_uses_template(self):
        response = self.client.get('/lists/the-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_show_all_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/lists/the-list/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')


class NewListTest(TestCase):

    def test_can_save_post_request(self):
        self.client.post('/lists/new', data={'item_text': 'New list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'New list item'})
        self.assertRedirects(response, '/lists/the-list/')


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


