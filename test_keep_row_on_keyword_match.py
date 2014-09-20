__author__ = 'Rachit'

# coding=utf-8
import unittest
import logging
import logging.config
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import settings

class KeepRowOnKeywordMatch(unittest.TestCase):
    '''
    functional test of the keep row on keyword match functionality
    '''

    logging.config.dictConfig(settings.LOGGING)
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = settings.BASE_TEST_URL
        self.verificationErrors = []

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def test_keep_row_on_keyword_match(self):
        '''
        Simple first test of positive case for splitting spreadsheet keeping row on keyword match
        :return:
        '''
        driver = self.driver

        #spreadsheet key
        test_spreadsheet_key = '?ss=10gSUMqKE4LJ5V8d8jsbQHL0oNaHUZ_fa6ZOPVwmJREg'

        self.logger.info('Starting test_keep_row_on_keyword_match')

        #load spreadsheet and perform test
        self.google_url = "https://www.gmail.com"
        driver.delete_all_cookies()
        driver.get(self.google_url)

        driver.find_element_by_id("Email").send_keys(settings.DEFAULT_GDRIVE_EMAIL)
        driver.find_element_by_id("Passwd").send_keys(settings.DEFAULT_GDRIVE_PW)
        driver.find_element_by_id("signIn").click()

        time.sleep(10)

        driver.get(self.base_url + test_spreadsheet_key)
        driver.switch_to.frame('donscraper')
        driver.find_element_by_xpath("//html/body/div/div[2]/ul/li[2]/a").click()

        time.sleep(10)

        driver.find_element_by_id("id_worksheet_name").clear()
        driver.find_element_by_id("id_worksheet_name").send_keys("Sheet1")
        driver.find_element_by_id("id_output_worksheet_name").clear()
        driver.find_element_by_id("id_output_worksheet_name").send_keys("Sheet1_remove")

        driver.find_element_by_id("id_column_to_search").clear()
        driver.find_element_by_id("id_column_to_search").send_keys("first_name")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("Tom")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys(settings.DEFAULT_GDRIVE_EMAIL)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(settings.DEFAULT_GDRIVE_PW)
        driver.find_element_by_xpath("//input[@class='btn btn-primary']").click()

        time.sleep(20)

        driver.find_element_by_id("id_worksheet_name").clear()
        driver.find_element_by_id("id_worksheet_name").send_keys("Sheet1_remove")
        driver.find_element_by_id("id_output_worksheet_name").clear()
        driver.find_element_by_id("id_output_worksheet_name").send_keys("Sheet1")

        driver.find_element_by_id("id_column_to_search").clear()
        driver.find_element_by_id("id_column_to_search").send_keys("first_name")
        driver.find_element_by_id("id_keywords").clear()
        driver.find_element_by_id("id_keywords").send_keys("Jake")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys(settings.DEFAULT_GDRIVE_EMAIL)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(settings.DEFAULT_GDRIVE_PW)
        driver.find_element_by_xpath("//input[@class='btn btn-primary']").click()

        time.sleep(20)

if __name__ == "__main__":
    unittest.main()