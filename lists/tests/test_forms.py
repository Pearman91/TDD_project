from unittest import skip

from django.test import TestCase

from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm
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
