# coding=utf-8
import unittest
import logging
import logging.config

from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import settings


class CompanySearch(unittest.TestCase):
    '''
    Suite of functional tests of the Company Search 2  functionality
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

    def test_company_search2(self):
        '''
        Simple first test of positive case for searching a single known domain for company details.
        :return:
        '''
        driver = self.driver

        #shared file
        test_domain_input = 'https://docs.google.com/a/hiplead.com/spreadsheets/d/1IgL_y_zkC7qs7ozjLSNv4qFmhnQo89opg4zL6idKfkQ/edit#gid=950033996'

        self.logger.info('Starting test_company_search2')

        #load page and search over special test values
        driver.get('%s%s' % (self.base_url, '/li/company/search2'))
        domains_gdoc_url_input = driver.find_element_by_id("id_domains_url")
        domains_gdoc_url_input.clear()
        domains_gdoc_url_input.send_keys(test_domain_input)
        driver.find_element_by_id('search_btn').click()

        #now wait for next page and validate results
        async_results_save_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "async_results_save"))
        )
        baseTable = driver.find_element_by_class_name("table-hover")
        table_rows = baseTable.find_elements_by_tag_name('tr')

        #row 0 is the header row
        row_tds = table_rows[1].find_elements_by_tag_name('td')
        current_job_company1 = row_tds[0]
        self.assertEquals(current_job_company1.text, 'Deem, Inc.')

        self.logger.info( 'Finished test_company_search2')

if __name__ == "__main__":
    unittest.main()
