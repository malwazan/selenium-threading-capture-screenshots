from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from traceback import print_stack
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from ..utilities import custom_logger as cl   # import custom_logger from utilities module
import logging
import time
import os
import random


class SeleniumDriver():
    # log initialization
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    # save screenshot method  
    def screenShot(self, resultMessage):
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)
        print(destinationDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")
            print_stack()


    # get page title
    def getTitle(self):
        return self.driver.title


    # get by type method
    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "classname":
            return By.CLASS_NAME
        elif locatorType == "linktest":
            return By.LINK_TEXT
        elif locatorType == "css_selector":
            return By.CSS_SELECTOR
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False


    # get element
    def getElement(self, locator, locatorType="xpath"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator + " and  locatorType: " + locatorType)
        except:
            self.log.warning("Element not found with locator: " + locator + " and  locatorType: " + locatorType)
        return element


    # get element within element instance
    def getElementWithinElement(self, locator, eInstance, locatorType="xpath"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = eInstance.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator + " and  locatorType: " + locatorType)
        except:
            self.log.warning("Element not found with locator: " + locator + " and  locatorType: " + locatorType)
        return element


    # element click
    def elementClick(self, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warning("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()


    # sendKeys(data) to element
    def sendKeys(self, data, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.clear()
            for c in data:
                element.send_keys(c)
                time.sleep(0.02)
            self.log.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warning("Cannot send data on the element with locator: " + locator +
                  " locatorType: " + locatorType)
            print_stack()


    # sendKeys(data) and press Enter
    def sendKeysAndPressEnter(self, data, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.clear()
            for c in data:
                element.send_keys(c)
                time.sleep(0.02)
            element.send_keys(Keys.RETURN)
            self.log.info("Entered data and press RETURN on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warning("Cannot send data on the element with locator: " + locator +
                  " locatorType: " + locatorType)
            print_stack()


    # check element presence (True/False)
    def isElementPresent(self, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False


    # check elementS presence - returns list of elements (True/False)
    def elementPresenceCheck(self, locator, locatorType="xpath"):
        try:
            byType = self.getByType(locatorType)
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False


    # wait for element to be located
    def waitForElementToBeLocated(self, locator, locatorType="xpath",
                               timeout=5, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be visible")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located((byType, locator)))
            self.log.info("Element with locator: "+ locator +" appeared on the web page")
        except:
            self.log.warning("Element with locator: "+ locator +" NOT appeared on the web page")
        return element


    # wait for Element within Element to be located
    def waitForElementWithinElementToBeLocated(self, locator, eInstance, locatorType="xpath",
                               timeout=5, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element Within Card to be visible")
            wait = WebDriverWait(eInstance, timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located((byType, locator)))
            self.log.info("Element appeared in the card with locator : " + locator + " : and locatorType : " + locatorType)
        except:
            self.log.warning("Element not appeared in the card with locator : " + locator + " : and locatorType : " + locatorType)
        return element


    # Wait for element to be located and click
    def waitForNavigationButtonToClick(self, locator, locatorType="xpath", 
                                         timeout=10, pollFrequency=0.5):
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be visible")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency)
            element = wait.until(EC.presence_of_element_located((byType, locator)))
            element.click()
            self.log.info("Navigation Button appeared on the web page and clicked")
        except:
            self.log.warning("Navigation Button not appeared on the web page and didn't clicked")
            print_stack()


    # wait for element to be clicked
    def waitForElementToBeClicked(self, locator, locatorType="xpath", 
                                         timeout=10, pollFrequency=0.5):
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency)
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warning("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    # wait for element within element to be clicked
    def waitForElementWithinElementToBeClicked(self, locator, eInstance, locatorType="xpath", 
                                                      timeout=10, pollFrequency=0.5):
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum : " + str(timeout) +
                  " : seconds for element within card to be clickable")
            wait = WebDriverWait(eInstance, timeout, poll_frequency=pollFrequency)
            element = wait.until(EC.element_to_be_clickable((byType, locator))).click()
            self.log.info("Clicked on element within card with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warning("Cannot click on the element within card locator: " + locator + " locatorType: " + locatorType)
            print_stack()


    # add explicit wait using time module
    def addExplicitWait(self, seconds):
        time.sleep(seconds)


    # click randomly on page
    def clickRandomlyOnPage(self, locator, xOffset, yOffset, locatorType="xpath"):
        refElement = self.getElement(locator=locator, locatorType="xpath")
        chain = ActionChains(self.driver)
        chain.move_to_element_with_offset(refElement, xOffset, yOffset)
        chain.click()
        chain.perform()


    # search for text in element
    def lookForText(self, locator, textString, locatorType="xpath"):
        element = self.getElement(locator=locator, locatorType=locatorType)
        return textString in element.text


    # add data to modal's field
    def addDataToModalField(self, modalInstance, fieldData, locator, locatorType="xpath", clearFields=False, timeout=5, pollFrequency=0.5):
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(modalInstance, timeout, poll_frequency=pollFrequency)
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            if clearFields == True:
                element.clear()
                """ work around not clearing fields """
                element.send_keys(" ")
                element.send_keys(Keys.BACKSPACE)
                """ end """
            for c in fieldData:
                element.send_keys(c)
                time.sleep(0.02)
            self.log.info("Entered: " + fieldData + " to: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.warning("Cannot Entered: " + fieldData + " to: " + locator + " and locatorType: " + locatorType)
            print_stack()


    # click modal button
    def clickModalButton(self, modalInstance, locator, locatorType="xpath", timeout=5, pollFrequency=0.5):
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(modalInstance, timeout, poll_frequency=pollFrequency)
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            element.click()
            self.log.info("Clicked on Modal's Button with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warning("Cannot click on Modal's Button with locator: " + locator + " locatorType: " + locatorType)
            print_stack()





    ######################################################## SCROLLING OF WEBPAGE

    # go to top of page
    def goTop(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    # web scroll
    def webScroll(self, direction="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
        # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")



