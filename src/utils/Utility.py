import os
import re
import signal

from selenium import webdriver
from selenium.common import WebDriverException, NoSuchDriverException


class Util:
    @staticmethod
    def get_chrome_driver(crx_name: str):
        options = webdriver.ChromeOptions()
        try:
            options.add_argument("--headless=new")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--no-sandbox')
            options.add_extension(f'./data/{crx_name}')
            return webdriver.Chrome(options=options)
        except (WebDriverException, NoSuchDriverException) as e:
            try:
                driver_path = "/usr/bin/chromedriver"
                service = webdriver.ChromeService(executable_path=driver_path)
                return webdriver.Chrome(service=service, options=options)
            except (WebDriverException, NoSuchDriverException) as e:
                raise RuntimeError(f'Could not start webdriver!')

    @staticmethod
    def shutdown():
        os.kill(os.getpid(), signal.SIGTERM)

    @staticmethod
    def convert_to_minutes(time_str: str):
        pattern = r'(\d+)\s*day[s]?,\s*(\d+)\s*hr[s]?,\s*(\d+)\s*min[s]?'
        match = re.match(pattern, time_str.strip())

        if not match:
            raise ValueError(f"Time string '{time_str}' is not in the expected format")

        days, hours, minutes = map(int, match.groups())

        total_minutes = days * 24 * 60 + hours * 60 + minutes
        return float(total_minutes)
