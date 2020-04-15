from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_preauthenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        # visit page so cookie can be set - 404 is fastest to visit
        self.browser.get(self.live_server_url + '/404-theres-no-such-thing')
        self.browser.add_cookie({'name': settings.SESSION_COOKIE_NAME,
                                 'value': session.session_key,
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

