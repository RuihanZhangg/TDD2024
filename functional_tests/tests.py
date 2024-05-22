from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import unittest
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
    
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_test = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_test)

        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Buy flowers')

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # table = self.browser.find_element(By.ID, 'id_list_table')
        # rows = table.find_elements(By.TAG_NAME, 'tr')
        # self.assertIn('1: Buy flowers', [row.text for row in rows])
        # self.assertIn('2: Give a gift to Lisi', [row.text for row in rows])

        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')
        
        
        self.fail('Finish the test!')



# assert 'Django' in browser.page_source