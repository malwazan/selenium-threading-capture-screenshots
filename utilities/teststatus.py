"""
@package utilities

CheckPoint class implementation
It provides functionality to assert the result

Example:
    self.check_point.markFinal("Test Name", result, "Message")
"""
from ..utilities import custom_logger as cl
import logging
from ..base.selenium_driver import SeleniumDriver
import allure
from allure_commons.types import AttachmentType

class TestStatus(SeleniumDriver):
    __test__ = False  # to notify pytest that this is not tests class

    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        super().__init__(driver)
        self.resultList = []

    def setResult(self, result, resultMessage):
        try:
            if result is not None:
                if result:
                    self.resultList.append("PASS")
                    self.log.info("### VERIFICATION SUCCESSFUL :: " + resultMessage)
                else:
                    self.resultList.append("FAIL")
                    self.log.info("### VERIFICATION FAILED :: " + resultMessage)
                    self.screenShot(resultMessage)  # if fail then take SS
                    allure.attach(self.driver.get_screenshot_as_png(), name=resultMessage, attachment_type=AttachmentType.PNG)
            else:
                self.resultList.append("FAIL")
                self.log.error("### VERIFICATION FAILED :: " + resultMessage)
                self.screenShot(resultMessage)
                allure.attach(self.driver.get_screenshot_as_png(), name=resultMessage, attachment_type=AttachmentType.PNG)
        except:
            self.resultList.append("FAIL")
            self.log.error("### Exception Occurred !!!")
            self.screenShot(resultMessage)  # if error then take SS
            allure.attach(self.driver.get_screenshot_as_png(), name=resultMessage, attachment_type=AttachmentType.PNG)

    def mark(self, result, resultMessage):
        """
        Mark the result of the verification point in a test case
        """
        self.setResult(result, resultMessage)

    def markFinal(self, testName, result, resultMessage):
        """
        Mark the final result of the verification point in a test case
        This needs to be called at least once in a test case
        This should be final test status of the test case
        """
        self.setResult(result, resultMessage)

        if "FAIL" in self.resultList:
            self.log.error(testName + "\n ### TEST FAILED ### \n")
            self.resultList.clear()
            assert True == False
        else:
            self.log.info(testName + "\n ### TEST SUCCESSFUL ### \n")
            self.resultList.clear()
            assert True == True