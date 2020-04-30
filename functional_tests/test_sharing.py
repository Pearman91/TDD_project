from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


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
        list_page = ListPage(self).add_list_item('Oprav trabanta')

        # there is option to share the list - he does that
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute('placeholder'),
                         'someone@example.com')
        list_page.share_list_with('jozin@example.com')

        # Jozin checks My Lists and see the shared lists
        self.browser = jozin_browser
        jozins_list = MyListsPage(self).go_to_my_lists_page()
        jozins_list.find_list_item('Oprav trabanta').click()

        # jozin check its Franta's list and he adds an item to it
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'franta@example.com'
        ))
        list_page.add_list_item('Kup Jozovi rum')

        # Franta can see the new item
        self.browser = franta_browser
        self.browser.refresh()
        list_page.wait_for_row_in_table('Kup Jozovi rum', 2)



