import re
from unittest import skip

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

TEST_EMAIL = 'hru3kus@gmail.com'
SUBJECT = 'Hi, you can log in to Superlists'


class LoginTest(FunctionalTest):

    @skip('manually works; local test works; staging test doesnt due to '
          'inability to check mail')
    def test_can_get_email_link_to_log_in(self):
        # go to homepage, and try to log in
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # show prompt to check mail
        self.wait_for(lambda: self.assertIn(
            'Check out your email',
            self.browser.find_element_by_tag_name('body').text))

        # check mail and find a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # find url link in the message
        self.assertIn('Link to log in:', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f"Didn't find url in email body: {email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # log in via clicking on the link
        self.browser.get(url)
        self.wait_to_be_logged_in(TEST_EMAIL)

        # log out
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(TEST_EMAIL)
