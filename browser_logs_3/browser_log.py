import json

import pytest
import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

DRIVERS = os.path.expanduser("~/Dev/drivers")


# https://github.com/SeleniumHQ/selenium/wiki/Logging

@pytest.fixture
def driver(request):
    caps = DesiredCapabilities.CHROME
    options = webdriver.ChromeOptions()
    options.add_experimental_option('w3c', False)
    caps['loggingPrefs'] = {
        'performance': 'ALL',
        'browser': 'ALL',
        'driver': 'ALL'
    }
    _driver = webdriver.Chrome(executable_path=f"{DRIVERS}/chromedriver",
                               desired_capabilities=caps,
                               options=options)

    request.addfinalizer(_driver.quit)
    return _driver


def test_logging_browser(driver):
    driver.get('https://ya.ru/')
    driver.execute_script("console.warn('Here is the WARNING message!')")
    driver.execute_script("console.error('Here is the ERROR message!')")
    driver.execute_script("console.log('Here is the LOG message!')")
    driver.execute_script("console.info('Here is the INFO message!')")
    print(driver.log_types)

    # Логирование производительности страницы
    performance_logs = []
    for line in driver.get_log("performance"):
        performance_logs.append(line)
    with open("performance.json", "w+") as f:
        f.write(json.dumps(performance_logs))

    # Логи консоли браузера, собирает WARNINGS, ERRORS
    browser_logs = []
    for line in driver.get_log("browser"):
        browser_logs.append(line)
    with open("browser.json", "w+") as f:
        f.write(json.dumps(browser_logs))

    # Локальное логирование драйвера
    driver_logs = []
    for line in driver.get_log("driver"):
        driver_logs.append(line)
    with open("driver.json", "w+") as f:
        f.write(json.dumps(driver_logs))
