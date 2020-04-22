import unittest
from unittest import skip
from unittest.mock import patch, Mock

from django.test import TestCase

from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, \
    ExistingListItemForm, ItemForm, NewListForm
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('class="form-control input-lg"', form.as_p())
        self.assertIn('placeholder="Just write down sth."', form.as_p())

    def test_form_validation_for_empty_item(self):
        form = ItemForm(data={'text': ''})
        # form.is_valid calls form.full_clean -> validation
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_saves_to_db(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'test this'})
        form.save(for_list=list_)
        self.assertEqual(Item.objects.all().count(), 1)


class ExistingListItemFormTest(TestCase):

    def text_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Just write down sth."', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='duplicitem', list=list_)
        form = ExistingListItemForm(for_list=list_, data={'text': 'duplicitem'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'sometext'})
        item = form.save()
        self.assertEqual(item, Item.objects.all()[0])


class NewListFormTest(unittest.TestCase):

    @skip('this is ugly version of the test - kept for comparison')
    @patch('lists.models.List')
    @patch('lists.models.Item')
    def test_creates_new_list_and_item_from_POST(self, mockItem, mockList):
        mock_item = mockItem.return_value
        mock_list = mockList.return_value
        user = Mock()
        form = NewListForm(data={'text': 'new list item'})

        form.is_valid()

        def check_item_text_and_list():
            self.assertEqual(mock_item.text, 'new list item')
            self.assertEqual(mock_item.list, mock_list)
            self.assertTrue(mock_list.save.called)
        mock_item.save.side_effect = check_item_text_and_list

        form.save(owner=user)

        self.assertTrue(mock_item.save.called)

    @patch('lists.forms.List.create_new')
    def test_save_form_creates_new_list_if_user_not_authenticated(
            self, mock_List_create_new
    ):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new list item'})
        form.is_valid()
        form.save(owner=user)

        mock_List_create_new.assert_called_once_with(
            first_item_text='new list item')

    @patch('lists.forms.List.create_new')
    def test_save_form_creates_new_list_if_user_authenticated(
            self, mock_List_create_new
    ):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new list item'})
        form.is_valid()
        form.save(owner=user)

        mock_List_create_new.assert_called_once_with(
            first_item_text='new list item', owner=user)

