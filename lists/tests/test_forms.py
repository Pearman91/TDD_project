from unittest import skip

from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, ItemForm


class ItemFormTest(TestCase):

    @skip('unfinished')
    def test_form_renders_text_input(self):
        form = ItemForm()
        self.fail(form.as_p())

    def test_form_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('class="form-control input-lg"', form.as_p())
        self.assertIn('placeholder="Just write down sth."', form.as_p())

    def test_form_validation_for_empty_item(self):
        form = ItemForm(data={'text': ''})
        # form.is_valid calls form.full_clean -> validation
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
