from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)

        # submit empty item and get appropriate error message
        self.browser.find_element_by_id('id_new_items').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'Nana, we won\'t let you put in empty items.'
        ))

        # submit non-empty item
        self.browser.find_element_by_id('id_new_items').send_keys(
            "Dance like nobody's watching")
        self.browser.find_element_by_id('id_new_items').send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Dance like nobody's watching")

        # for the 2nd time submit empty item and get error message
        self.browser.find_element_by_id('id_new_items').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'Nana, we won\'t let you put in empty items.'
        ))

        # add one more correct item and check both items
        self.browser.find_element_by_id('id_new_items').send_keys(
            "And sing like nobody's listening")
        self.browser.find_element_by_id('id_new_items').send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Dance like nobody's watching")
        self.wait_for_row_in_table("2: And sing like nobody's listening")


        self.fail('Write this test, dammit!')

