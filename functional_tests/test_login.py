import os
import poplib
import re
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = 'Hi, you can log in to Superlists'


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ.get('YAHOO_PASSWORD'))
            while time.time() - start < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # go to homepage, and try to log in
        if self.staging_server:
            test_email = 'radiofriendlyface@yahoo.com'
        else:
            test_email = 'jozizbazin@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # show prompt to check mail
        self.wait_for(lambda: self.assertIn(
            'Check out your email',
            self.browser.find_element_by_tag_name('body').text))

        # check mail and find a message
        body = self.wait_for_email(test_email, SUBJECT)

        # find url link in the message
        self.assertIn('Link to log in:', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f"Didn't find url in email body: {body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # log in via clicking on the link
        self.browser.get(url)
        self.wait_to_be_logged_in(test_email)

        # log out
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(test_email)
