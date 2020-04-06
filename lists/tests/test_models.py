from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first bloody item in da list'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item in the list'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,
                         'The first bloody item in da list')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'The second item in the list')
        self.assertEqual(second_saved_item.list, list_)

    def test_cannot_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)

        # try to run 'item.save()' save and expcet ValidationError
        # otherwise fail
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

