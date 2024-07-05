import time
from typing import Optional

import requests
from selenium.common import WebDriverException, NoSuchDriverException, NoSuchElementException
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from core.Handler.Exception import HandlerException
from core.Metrics import Metrics
from utils.Utility import Util


class GrassHandler:
    def __init__(self, driver: ChromiumDriver, extension_id: str):
        self.driver: ChromiumDriver = driver
        self.extension_id: str = extension_id
        self.ip = requests.get('https://ident.me/').content.decode('utf-8')

    def quit(self) -> None:
        if self.driver is not None:
            self.driver.quit()
        print('webdriver stopped')

    def connect(self, username: str, password: str) -> None:
        # find login form
        if not self.__login_to_grass(username, password):
            raise HandlerException("Failed to find login form")
        if not self.__check_login():
            raise HandlerException("Failed to login")
        if not self.__check_connected():
            raise HandlerException("Can not connect to Grass")
        if not self.__check_metrics():
            raise HandlerException("Failed to get metrics on startup")

    def get_metrics(self) -> Optional[Metrics]:
        total_wait = 5
        wait_time = 0
        time_to_wait = 0.2

        self.driver.refresh()
        while wait_time < total_wait:
            try:
                return self.__get_metric_from_page()
            except (WebDriverException, NoSuchElementException):
                wait_time += time_to_wait
                time.sleep(time_to_wait)
        return None

    def __check_connected(self) -> bool:
        total_wait = 5
        wait_time = 0
        time_to_wait = 0.2

        self.driver.get(f'chrome-extension://{self.extension_id}/index.html')
        while wait_time <= total_wait:
            try:
                self.driver.find_element('xpath', '//*[contains(text(), "Grass is Connected")]')
                return True
            except (WebDriverException, NoSuchDriverException):
                wait_time += time_to_wait
                time.sleep(time_to_wait)
        return False

    def __check_metrics(self) -> bool:
        total_wait = 5
        wait_time = 0
        time_to_wait = 0.2

        self.driver.get('https://app.getgrass.io/dashboard/networks')
        while wait_time <= total_wait:
            try:
                self.__get_metric_from_page()
                return True
            except (WebDriverException, NoSuchElementException) as e:
                wait_time += time_to_wait
                time.sleep(time_to_wait)
        return False

    def __get_metric_from_page(self) -> Metrics:
        node_elem = self.driver.find_element('xpath', f"//tr[td[3]//*[contains(text(), '{self.ip}')]]")

        node_name = node_elem.find_element('xpath', 'td[2]').text
        time_connected = node_elem.find_element('xpath', 'td[4]').text
        network_quality = float(node_elem.find_element('xpath', 'td[5]').text.replace("%", ""))
        node_earnings = float(node_elem.find_element('xpath', 'td[6]').text.replace("K", ""))

        return Metrics(node_name, Util.convert_to_minutes(time_connected), network_quality, node_earnings)

    def __login_to_grass(self, username, password) -> bool:
        total_wait = 5
        wait_time = 0
        time_to_wait = 0.2

        self.driver.get('https://app.getgrass.io/')
        while wait_time <= total_wait:
            try:
                user_input = self.driver.find_element('xpath', '//*[@name="user"]')
                password_input = self.driver.find_element('xpath', '//*[@name="password"]')
                submit_button = self.driver.find_element('xpath', '//*[@type="submit"]')
                user_input.send_keys(username)
                password_input.send_keys(password)
                submit_button.click()
                return True
            except (WebDriverException, NoSuchElementException):
                wait_time += time_to_wait
                time.sleep(time_to_wait)
        return False

    def __check_login(self):
        total_wait = 5
        wait_time = 0
        time_to_wait = 0.2

        while wait_time <= total_wait:
            try:
                self.driver.find_element('xpath', '//*[contains(text(), "Dashboard")]')
                return True
            except (NoSuchElementException, WebDriverException):
                wait_time += time_to_wait
                time.sleep(time_to_wait)
        return False
