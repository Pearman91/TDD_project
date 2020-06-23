from selenium.webdriver.common.keys import Keys

from .base import wait


class ListPage(object):

    def __init__(self, test):
        self.test = test

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name="share"]')

    def get_table_rows(self):
        return self.test.browser.find_elements_by_css_selector(
            '#id_list_table tr')

    def get_item_input_box(self):
        return self.test.browser.find_element_by_id('id_text')

    def get_list_owner(self):
        return self.test.browser.find_element_by_id('id_list_owner').text

    def get_shared_with_list(self):
        return self.test.browser.find_elements_by_css_selector('.list-share')

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))

    @wait
    def wait_for_row_in_table(self, item_text, item_number):
        expected_row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(expected_row_text, [row.text for row in rows])

    def add_list_item(self, item_text):
        num_rows = len(self.get_table_rows())
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        items_number = num_rows + 1
        self.wait_for_row_in_table(item_text, items_number)
        return self

