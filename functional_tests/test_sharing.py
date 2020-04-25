from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_list_with_another_user(self):
        # Franta logs in
        self.create_preauthenticated_session('franta@example.com')
        franta_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(franta_browser))

        # Jozin logs in diferent browser
        jozin_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(jozin_browser))
        self.browser = jozin_browser
        self.create_preauthenticated_session('jozin@example.com')

        # Franta starts a list
        self.browser = franta_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Oprav trabanta')

        # there is option to share list
        share_box = self.browser.find_element_by_css_selector(
            'input[name="share"]')
        self.assertEqual(share_box.get_attribute('placeholder'),
                         'someone@example.com')


