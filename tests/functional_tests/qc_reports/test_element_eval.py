import unittest
import os
import time

from ConfigParser import SafeConfigParser

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class ElementEvalTest(unittest.TestCase):
    def setUp(self):
        parser = SafeConfigParser()
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        parser.read(config_path + '/config.ini')

        binary = FirefoxBinary(parser.get('webdriver', 'firefox_binary'))

        self.browser = webdriver.Firefox(firefox_binary=binary)

        self.target_website = parser.get('url', 'test')

        username = parser.get('login', 'username')
        password = parser.get('login', 'password')

        self.login(username, password)

    def tearDown(self):
        self.browser.quit()

    def login(self, username, password):
        self.browser.get(self.target_website)

        username_field = self.browser.find_element_by_name('login')
        password_field = self.browser.find_element_by_name('password')
        submit_field = self.browser.find_element_by_name('Submit')

        username_field.send_keys(username)
        password_field.send_keys(password)

        submit_field.submit()

    def test_load_element_eval_page(self):
        self.browser.get(self.target_website)

        time.sleep(5)

        element_eval_link = self.browser.find_element_by_xpath('//div[@spt_title="Report"]')
        element_eval_link.click()

        element_eval_header = self.browser.find_element_by_class_name('spt_tab_header_label')
        self.assertEqual('Report', element_eval_header.text)




if __name__ == '__main__':
    unittest.main()
