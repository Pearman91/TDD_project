from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_preauthenticated_session

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_preauthenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_preauthenticated_session(email)

        # visit page so cookie can be set - 404 is fastest to visit
        self.browser.get(self.live_server_url + '/404-theres-no-such-thing')
        self.browser.add_cookie({'name': settings.SESSION_COOKIE_NAME,
                                 'value': session_key,
                                 'path': '/',
                                 })

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
        self.wait_for(lambda:
                      self.browser.find_element_by_link_text('Buy groceries'))
        self.browser.find_element_by_link_text('Buy groceries').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url,
                                               second_list_url))

        # after logging out, there are no 'My lists' anymore
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_link_text('My lists'),
            []
        ))


