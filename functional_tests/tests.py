import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        # Is there the right h1 tag text?
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Is there a right element for adding items?
        inputbox = self.browser.find_element_by_id('id_new_items')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Just write down sth.')

        # user adds item
        inputbox.send_keys('Buy new shoes')  # selenium input
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.find_row_in_table('1: Buy new shoes')

        # user adds another item
        inputbox = self.browser.find_element_by_id('id_new_items')
        inputbox.send_keys('Put the shoes on your ears')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Are the items added to the table?
        self.find_row_in_table('1: Buy new shoes')
        self.find_row_in_table('2: Put the shoes on your ears')

        self.fail('You still have work to do here, dude!')

    def find_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows],
                      f"New item '{row_text}' was not added to the list.")

