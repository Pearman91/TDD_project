import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retreive_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

        # Is there the right h1 tag text?
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Is there a right element for adding items?
        inputbox = self.browser.find_element_by_id('id_new_items')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Enter a To-Do item')

        # user adds item
        inputbox.send_keys('Buy new shoes')  # selenium input
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Is there table with newly added item?
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy new shoes') for row in rows)

        # TODO: chapter 04


if __name__ == '__main__':
    # starts the test runner tht find and executes test methods in test classes
    unittest.main(warnings='ignore')
