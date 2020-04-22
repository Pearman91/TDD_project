from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


User = get_user_model()


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()

        self.assertIn(item, list_.item_set.all())

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text='item1', list=list_)
        item2 = Item.objects.create(text='item2', list=list_)
        item3 = Item.objects.create(text='item3', list=list_)
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_cannot_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)

        # try to run 'item.save()' save and expcet ValidationError
        # otherwise fail
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_in_one_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='Duplicitem', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='Duplicitem', list=list_)
            item.full_clean()

    def test_one_item_in_multiple_lists_is_valid(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text='Duplicitem', list=list1)
        item = Item(text='Duplicitem', list=list2)
        item.full_clean()  # if this goes well, Validation error is not raised


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_can_save_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_list_can_have_owner(self):
        List(owner=User())

    def test_list_dont_have_to_have_owner(self):
        List().full_clean()

    def test_create_new_returns_new_list(self):
        returned_list = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()

        self.assertEqual(returned_list, new_list)

    def test_list_named_ater_first_item(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='firstey')
        Item.objects.create(list=list_, text='secondey')
        self.assertEqual(list_.name, 'firstey')

