from ..pages.users_page import UsersPage
from ..utilities.teststatus import TestStatus
from ..utilities import custom_logger as cl
import logging
import unittest
import pytest
import os
from threading import Thread
from ..utilities.screenshot import capture_screenshot


@pytest.mark.usefixtures("oneTimeSetUp")
class UsersTests(unittest.TestCase):

	log = cl.customLogger(logging.DEBUG)

	@pytest.fixture(autouse=True)
	def classSetup(self, request, oneTimeSetUp):
		self.usersPage   = UsersPage(self.driver)
		self.testStatus = TestStatus(self.driver)

		# launch thread for taking screenshots
		stop_thread = False
		ss_path = f"screenshots/{ str( request.node.nodeid.split('::')[-1] ) }/"
		if not os.path.exists(ss_path): os.makedirs(ss_path)
		thread = Thread(target=capture_screenshot, kwargs={"driver": self.driver, "ss_path": ss_path, "stop_thread": lambda: stop_thread})
		thread.start()

		yield

		# destroy screenshots thread
		stop_thread = True


	@pytest.mark.run(order=1)
	def test_check_google(self):
		self.log.info("Testing... google")
		self.usersPage.navigate_to_google()
		self.testStatus.markFinal(testName="Verify google search engine", result=True, 
			resultMessage="check google search engine opened")


	@pytest.mark.run(order=2)
	def test_check_youtube(self):
		self.log.info("Testing... youtube")
		self.usersPage.navigate_to_youtube()
		self.testStatus.markFinal(testName="Verify youtube", result=True, 
			resultMessage="check youtube opened")