import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope='class')
def oneTimeSetUp(request, browser):
	print("\nBeginning of Tests")

	# set driver browser
	if browser == "firefox":
		driver = webdriver.Firefox(executable_path="geckodriver.exe")
	elif browser == "iexplorer":
		driver = webdriver.Ie()
	else:
		#options = ChromeOptions()
		#options.add_experimental_option('excludeSwitches', ['enable-logging'])
		chrome_service = Service(os.getenv("CHROME_DRIVER_PATH"))
		driver = webdriver.Chrome(service=chrome_service)

	driver.maximize_window()

	if request.cls is not None:
		request.cls.driver = driver

	yield driver

	driver.quit()


def pytest_addoption(parser):
	parser.addoption("--browser")
	parser.addoption("--osType", help="Type of operating system")

@pytest.fixture(scope="session")
def browser(request):
	return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def osType(request):
	return request.config.getoption("--osType")