from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
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
        self.wait_for_row_in_table('1: Buy new shoes')

        # user adds another item
        inputbox = self.browser.find_element_by_id('id_new_items')
        inputbox.send_keys('Put the shoes on your ears')
        inputbox.send_keys(Keys.ENTER)

        # Are the items added to the table?
        self.wait_for_row_in_table('1: Buy new shoes')
        self.wait_for_row_in_table('2: Put the shoes on your ears')

    def test_multiple_users_can_start_list_at_different_url(self):
        # first user - start the list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_items')
        inputbox.send_keys('Buy new shoes')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy new shoes')

        # first user - read the list
        first_user_url = self.browser.current_url
        self.assertRegex(first_user_url, '/lists/.+')

        ## second user wants to create list - new browser session to get rid of
        ## cookies and stuff
        ## this is meta-comment for developer, nothin to do with User Story
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # check the 2nd user doesnt see items from 1st user
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new shoes', page_text)
        self.assertNotIn('Put the shoes on your ears', page_text)

        # second user - start new list
        inputbox = self.browser.find_element_by_id('id_new_items')
        inputbox.send_keys('Climb Mt. Everest')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Climb Mt. Everest')

        # second user - read the list
        second_user_url = self.browser.current_url
        self.assertRegex(second_user_url, '/lists/.+')
        self.assertNotEqual(second_user_url, first_user_url)

        # check 2nd user still seems only his own item
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Climb Mt. Everest', page_text)
        self.assertNotIn('Buy new shoes', page_text)

