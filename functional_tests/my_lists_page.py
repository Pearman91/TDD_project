class MyListsPage(object):

    def __init__(self, test):
        self.test = test

    def find_list_item(self, item):
        return self.test.browser.find_element_by_link_text(item)

    def go_to_my_lists_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element_by_link_test('My lists').click()
        self.test.wait_for(lambda: self.test.assertEqual(
            self.test.browser.find_element_by_tag_name('h1').text,
            'My lists'
        ))
        return self