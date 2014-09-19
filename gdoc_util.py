# coding=utf-8

import gdata.data
import gdata.docs.data
import gdata.docs.client
import gdata.acl.data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xmltodict

import CONTENT_TYPE
import settings


client = None

def getGDriveClient(email=settings.DEFAULT_GDRIVE_EMAIL, password=settings.DEFAULT_GDRIVE_PW):
    client = gdata.docs.client.DocsClient(source='MyTest')
    client.api_version = "3"
    client.ssl = True
    client.ClientLogin(email, password, client.source)
    return client

def _upload_file_to_gdrive( file_path, file_name='NAME NOT SET', file_type=CONTENT_TYPE.TSV):
    '''

    :param file_path: Must include dot notation for root directly. For example: './cleanertest1.xlsx'
    :param file_name:
    :return:
    '''
    client = getGDriveClient()
    filePath = file_path
    newResource = gdata.docs.data.Resource(
        filePath, "%s" % (file_name)
    )
    media = gdata.data.MediaSource()
    media.SetFileHandle(filePath, file_type)
    newDocument = client.CreateResource(newResource, create_uri=gdata.docs.client.RESOURCE_UPLOAD_URI, media=media)
    return newDocument


def upload_file_to_gdrive(file_name, gdoc_name, file_type=CONTENT_TYPE.TSV):
    doc = _upload_file_to_gdrive(file_name, gdoc_name, file_type)
    obj = xmltodict.parse(str(doc))
    ss_key_node = obj['ns0:entry']['ns1:resourceId']
    ss_key = ss_key_node.split(':')[1]
    return ss_key

def login_gdrive(driver, email=settings.DEFAULT_GDRIVE_EMAIL, password=settings.DEFAULT_GDRIVE_PW):
    driver.get('https://drive.google.com')
    driver.find_element_by_id("Email").send_keys(email)
    driver.find_element_by_id("Passwd").send_keys(password)
    driver.find_element_by_id('signIn').click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "doclist"))
    )
