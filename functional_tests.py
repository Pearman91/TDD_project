from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retreive_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail(
            'Finish the test - there are still things that have to be tested!')


if __name__ == '__main__':
    # starts the test runner tht find and executes test methods in test classes
    unittest.main(warnings='ignore')
