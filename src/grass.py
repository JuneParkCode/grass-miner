import os
import re
import signal
import time

import requests
from selenium import webdriver
from selenium.common import WebDriverException, NoSuchDriverException, NoSuchElementException
from selenium.webdriver.chrome.service import Service

from prometheus import Prometheus

TRY = 5
prometheus = Prometheus()


class Grass:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        self.driver = None
        self.ip = None
        self.options = None
        self.crx_name = None
        self.extension_id = None
        self.username = None
        self.password = None
        self.metrics = None

    def init(self):
        try:
            self.username: str = os.environ['GRASS_USER']
            self.password: str = os.environ['GRASS_PASSWORD']
            self.extension_id: str = os.environ['GRASS_CRX_EXTENSION_ID']
            self.crx_name: str = os.environ['GRASS_CRX_NAME']

            if self.username is "" or self.password is "" or self.extension_id is "" or self.crx_name is "":
                self.shutdown()
        except:
            print('invalid environment variables')
            self.shutdown()

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument('--no-sandbox')
        self.options.add_extension(f'./data/{self.crx_name}')
        self.ip = requests.get('https://ident.me/').content.decode('utf-8')
        # init driver
        try:
            if self.driver is not None:
                self.driver.quit()
            self.driver = webdriver.Chrome(options=self.options)
        except (WebDriverException, NoSuchDriverException) as e:
            print('Could not start with webdriver Manager!')
            try:
                driver_path = "/usr/bin/chromedriver"
                service = Service(executable_path=driver_path)
                self.driver = webdriver.Chrome(service=service, options=self.options)
            except (WebDriverException, NoSuchDriverException) as e:
                print('Chrome Driver not found!')
                self.shutdown()
        print('webdriver started')

    def start(self):
        self.init()
        try:
            if not self.__login():
                print('login failed')
                self.shutdown()
            if not self.__check_connection():
                print('connection failed')
                self.shutdown()

            # to get metrics.
            self.driver.get('https://app.getgrass.io/dashboard/networks')
            time.sleep(3)
            self.__set_prometheus_metric()
        except Exception as e:
            print("An error occurred during startup.")
            print(e)
            self.shutdown()

    def shutdown(self):
        self.__save_error("shutdown", "shutdown progress...")
        print("shutdown app")
        if self.driver is not None:
            self.driver.quit()
        os.kill(os.getpid(), signal.SIGTERM)

    def get_metrics(self):
        # get node table
        self.driver.refresh()

        try_count = 1
        while try_count <= TRY:
            try:
                time.sleep(1)

                node_elem = self.driver.find_element('xpath', f"//tr[td[3]//*[contains(text(), '{self.ip}')]]")

                time_connected = node_elem.find_element('xpath', 'td[4]').text
                network_quality = float(node_elem.find_element('xpath', 'td[5]').text.replace("%", ""))
                node_earnings = float(node_elem.find_element('xpath', 'td[6]').text.replace("K", ""))

                self.metrics = {
                    "time_connected": self.__convert_to_minutes(time_connected),
                    "network_quality": network_quality,
                    "node_earnings": node_earnings
                }
                return self.metrics
            except Exception as e:
                try_count += 1

        self.__save_error("metric_fail", "failed to fetch metrics")
        return self.metrics

    def __login(self):
        print('login...')

        self.driver.get('https://app.getgrass.io/')
        # find login form
        login_form = self.__find_login_form()
        if not login_form:
            return False
        if not self.__send_login_form(login_form):
            return False
        if not self.__check_login():
            return False
        return True

    def __find_login_form(self):
        for i in range(TRY):
            try:
                user_input = self.driver.find_element('xpath', '//*[@name="user"]')
                password_input = self.driver.find_element('xpath', '//*[@name="password"]')
                submit_button = self.driver.find_element('xpath', '//*[@type="submit"]')
                print('login form found')
                return user_input, password_input, submit_button
            except (WebDriverException, NoSuchElementException) as e:
                print(f'try to find login form.  try: {i + 1} times')
                time.sleep(3)

        self.__save_error("login_fail", "failed to find login form")
        return False

    def __send_login_form(self, login_form):
        user_input, password_input, submit_button = login_form
        try:
            # get user from env
            user_input.send_keys(self.username)
            password_input.send_keys(self.password)
            submit_button.click()
            print('login form sent')
            return True
        except (WebDriverException, NoSuchElementException) as e:
            self.__save_error("login_fail", "failed to send login form")
            return False

    def __check_login(self):
        time.sleep(1)
        for i in range(15):
            try:
                self.driver.find_element('xpath', '//*[contains(text(), "Dashboard")]')
                print('check login success')
                return True
            except:
                print(f'try to login {i + 1}')
                time.sleep(1)
        self.__save_error("login_fail", "failed to check login")
        return False

    def __check_connection(self):
        for i in range(TRY):
            try:
                self.driver.get(f'chrome-extension://{self.extension_id}/index.html')
                time.sleep(2)
                self.driver.find_element('xpath', '//*[contains(text(), "Grass is Connected")]')
            except:
                print(f'check connections... {i + 1}')
                time.sleep(1)
            return True
        self.__save_error("connection_fail", "failed to check connections")
        return False

    def __set_prometheus_metric(self):
        # get node table
        try:
            node_elem = self.driver.find_element('xpath', f"//tr[td[3]//*[contains(text(), '{self.ip}')]]")

            node_name = node_elem.find_element('xpath', 'td[2]').text
            time_connected = node_elem.find_element('xpath', 'td[4]').text
            network_quality = float(node_elem.find_element('xpath', 'td[5]').text.replace("%", ""))
            node_earnings = float(node_elem.find_element('xpath', 'td[6]').text.replace("K", ""))

            prometheus.init(node_name, self.ip)
            self.metrics = {
                "node_name": node_name,
                "time_connected": time_connected,
                "network_quality": network_quality,
                "node_earnings": node_earnings
            }
            return self.metrics
        except Exception as e:
            self.__save_error("set_prometheus_metric", "failed to set prometheus metrics")
            return None

    def __convert_to_minutes(self, time_str):
        pattern = r'(\d+)\s*day[s]?,\s*(\d+)\s*hr[s]?,\s*(\d+)\s*min[s]?'
        match = re.match(pattern, time_str.strip())

        if not match:
            raise ValueError(f"Time string '{time_str}' is not in the expected format")

        days, hours, minutes = map(int, match.groups())

        total_minutes = days * 24 * 60 + hours * 60 + minutes
        return float(total_minutes)

    def __save_error(self, error_name, error_message):
        self.driver.save_screenshot(f'./data/error/{error_name}.png')
        print(error_message)
