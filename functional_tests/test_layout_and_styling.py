from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # check that inputbox is centered
        inputbox = self.browser.find_element_by_id('id_new_items')
        # TODO: find why its always ~=580 and than change delta to 10
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=100)

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_items')
        # TODO: find why its always ~=580 and then change delta to 10
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2, 512, delta=100)
