from unittest import skip
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, \
    ExistingListItemForm
from lists.models import Item, List

User = get_user_model()


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html_with_test_client(self):
        """ Use Django Test Client. Testing of html content = testing constants,
         which is wrong. Test whether the correct template was used, instead.
         We don't need to decode html content here.
         """
        response = self.client.get('/')

        # behold the magic power of Django's test client!
        self.assertTemplateUsed(response, 'index.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_list_uses_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_show_all_items_from_given_list(self):
        given_list = List.objects.create()
        Item.objects.create(text='item1', list=given_list)
        Item.objects.create(text='item2', list=given_list)

        other_list = List.objects.create()
        Item.objects.create(text='item3', list=other_list)
        Item.objects.create(text='item4', list=other_list)

        response = self.client.get(f'/lists/{given_list.id}/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'item3')
        self.assertNotContains(response, 'item4')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': 'Added item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Added item')
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': 'Added item'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_for_invalid_item_not_saved_in_db(self):
        self.post_empty_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_item_redirection_status_code(self):
        response = self.post_empty_input()
        self.assertEqual(response.status_code, 200)

    def test_for_invalid_item_redirection_template(self):
        response = self.post_empty_input()
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_item_error_message(self):
        response = self.post_empty_input()
        expected_error = escape("Nana, we won't let you put in empty items.")
        self.assertContains(response, expected_error)

    def test_duplicate_item_validation_errors_returns_to_list_page(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='sometext', list=list_)

        # try to post item with same text
        response = self.client.post(
            f'/lists/{list_.id}/', data={'text': 'sometext'})

        expected_error = DUPLICATE_ITEM_ERROR
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_shows_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_empty_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def post_empty_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text': ''})


class NewListTest(TestCase):

    def test_can_save_post_request(self):
        self.client.post('/lists/new', data={'text': 'New list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'text': 'New list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_error_redirect_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_validation_error_message(self):
        response = self.client.post('/lists/new', data={'text': ''})
        # escape() is for django handling of strings with funky characters
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_validation_error_puts_form_in_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_items_are_not_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    @patch('lists.views.List')
    @patch('lists.views.ItemForm')  # mock List needs mock ItemForm
    def test_list_owner_is_saved_if_user_is_authenticated(
            self, mockItemFormClass, mockListClass
    ):
        user = User.objects.create(email='franta@trabanta.cz')
        self.client.force_login(user)
        # list instance
        mock_list = mockListClass.return_value

        def check_owner_assigned():
            self.assertEqual(mock_list.owner, user)
        mock_list.save.side_effect = check_owner_assigned

        self.client.post('/lists/new', data={'text': 'mhmm...sandwiches'})

        mock_list.save.assert_called_once_with()


class MyListsTest(TestCase):

    def test_my_list_url_renders_my_lists_template(self):
        email = 'franta@trabanta.cz'
        User.objects.create(email=email)
        response = self.client.get(f'/lists/users/{email}/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_user_to_template(self):
        email = 'franta@trabanta.cz'
        User.objects.create(email='wrong@user.com')
        correct_user = User.objects.create(email=email)
        response = self.client.get(f'/lists/users/{email}/')
        self.assertEqual(response.context['owner'], correct_user)

