from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):

    def test_logged_in_user_save_lists_as_my_lists(self):
        # user logs in
        email = 'jozinzbazin@example.com'
        self.create_preauthenticated_session(email)

        # user creates list with 2 items
        self.browser.get(self.live_server_url)
        self.add_list_item('Stay home')
        self.add_list_item('Dont wank too much')
        first_list_url = self.browser.current_url

        # user clicks on 'My lists'
        self.browser.find_element_by_link_text('My lists').click()

        # the user-created list is here, named after its first item
        self.wait_for(lambda: self.browser.find_element_by_link_text('Stay home'))
        self.browser.find_element_by_link_text('Stay home').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url,
                                               first_list_url))

        # user creates another list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy groceries')
        second_list_url = self.browser.current_url

        # user clicks on 'My list' and see the new list, too
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda:
                      self.browser.find_element_by_link_text('Buy groceries'))
        self.browser.find_element_by_link_text('Buy groceries').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url,
                                               second_list_url))

        # after logging out, there are no 'My lists' anymore
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))

