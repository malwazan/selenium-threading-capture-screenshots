from selenium.webdriver.common.by import By
from ..base.selenium_driver import SeleniumDriver
from ..utilities import custom_logger as cl
import logging
import time


class UsersPage(SeleniumDriver):

	log = cl.customLogger(logging.DEBUG)

	def __init__(self, driver):
		super().__init__(driver)
		self.driver = driver


	def navigate_to_google(self):
		self.driver.get("http://google.com")
		time.sleep(5)

	def navigate_to_youtube(self):
		self.driver.get("http://youtube.com")
		time.sleep(5)
