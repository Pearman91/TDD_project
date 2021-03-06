from unittest import skip

from selenium.webdriver.common.keys import Keys

from lists.forms import DUPLICATE_ITEM_ERROR
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)

        # submit empty item and get html5 error message
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'))

        # submit non-empty item
        self.get_item_input_box().send_keys("Dance like nobody's watching")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Dance like nobody's watching")

        # for the 2nd time submit empty item and get error message
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'))

        # add one more correct item and check both items
        self.get_item_input_box().send_keys("And sing like nobody's listening")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Dance like nobody's watching")
        self.wait_for_row_in_table("2: And sing like nobody's listening")

    def test_cannot_add_duplicate_item(self):
        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys("Let's duplicate")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Let's duplicate")

        self.get_item_input_box().send_keys("Let's duplicate")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            DUPLICATE_ITEM_ERROR))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys("Duplicator")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Duplicator")

        # duplicate item entry
        self.get_item_input_box().send_keys("Duplicator")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()))

        self.get_item_input_box().send_keys('a')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()))

    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")
