import logging
import logging.config
import unittest

import gspread
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import gdoc_util
import settings

class ContactKeyCreator(unittest.TestCase):
    '''
    Suite of functional tests of the contact key creator functionality.
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

    def test_contact_key_creator(self):
        '''
        Test the simple positive case for creation of a single functioning contact key.
        :return:
        '''
        self.logger.info('Starting test_contact_key_creator')

        #setup the doc on gdrive first
        file_name = 'ContactKeyTest1'
        ss_key = gdoc_util.upload_file_to_gdrive('contact_key_test1.tsv', file_name)
        driver = self.driver
        gdoc_util.login_gdrive(driver)
        driver.get('%s%s' % (self.base_url, '?ss=' + ss_key))

        gc = gspread.login(settings.DEFAULT_GDRIVE_EMAIL, settings.DEFAULT_GDRIVE_PW)
        my_worksheet = gc.open_by_key(ss_key).sheet1
        e2_val = my_worksheet.acell('E2')
        self.logger.info('e2_val: %s' % e2_val)
        #reset the cell
        my_worksheet.update_acell('E2', '')
        e2_val = my_worksheet.acell('E2')
        self.logger.info('e2_val reset to: %s' %e2_val)

        #now run the command
        #switch to input form frame
        driver.switch_to.frame(0)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Hiplead"))
        ).click()

        id_worksheet_name_INPUT = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_worksheet_name"))
        )

        id_worksheet_name_INPUT.clear()
        id_worksheet_name_INPUT.send_keys(file_name)

        Select(driver.find_element_by_id("id_scrapers")).select_by_value('contactKeyCreator')
        driver.find_element_by_id("id_email").send_keys(settings.DEFAULT_GDRIVE_EMAIL)
        driver.find_element_by_id("id_password").send_keys(settings.DEFAULT_GDRIVE_PW)

        #ok, now submit the form
        id_worksheet_name_INPUT.submit()

        #then wait for task to complete
        #this success alert only becomes visible when task is actually finished.
        success_div = driver.find_element_by_class_name('time_remaining')
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of(success_div)
            )
        except StaleElementReferenceException as e:
            #TODO The javascript DOM manipulation that results in StaleElementReferenceException needs to be resolved.
            success_div = driver.find_element_by_class_name('time_remaining')
            WebDriverWait(driver, 10).until(
                EC.visibility_of(success_div)
            )

        #now validate cell value, since we know task has completed.
        e2_val = my_worksheet.acell('E2')
        self.logger.info('e2_val after test: %s' %e2_val)
        self.assertEquals('john_franklin_smith_somedomain.net', e2_val.value)

        self.logger.info( 'Finished test_contact_key_creator')


if __name__ == "__main__":
    unittest.main()
