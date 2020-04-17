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
        email = 'jozinzbazin@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # log in
        self.create_preauthenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

