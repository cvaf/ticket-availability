from datetime import date, timedelta, datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

from typing import List


INTERESTED_DATES = (date.today(), date(2021, 12, 9))


class Ticket:

    URL = "https://shop.tate.org.uk/ticket/date?cgid=7811"
    BUTTON_XPATH = '//*[@id="cboxLoadedContent"]/div/div[2]/div[3]/div[2]/a'

    def __init__(self):
        return

    def _get_browser(self) -> WebDriver:
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        return webdriver.Firefox(options=firefox_options)

    def get_page_source(self) -> BeautifulSoup:
        browser = self._get_browser()
        browser.get(self.URL)
        sleep(1)
        browser.find_element("xpath", self.BUTTON_XPATH).click()
        sleep(3)
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.quit()
        return soup

    def _check_date_status(self, soup: BeautifulSoup, date: str) -> bool:
        return False if "SOLD" in soup.find("div", {"data-full": date}).text else True

    def check_availability(self) -> List[str]:
        soup = self.get_page_source()
        return [
            d.strftime("%Y-%m-%d")
            for d in _find_dates(*INTERESTED_DATES)
            if self._check_date_status(soup, f"{d.year}-{d.month-1}-{d.day}")
        ]


def _find_dates(start_date: date, end_date: date) -> List[date]:
    if datetime.now().hour > 15:
        start_date += timedelta(days=1)

    delta = (end_date - start_date).days + 1
    return [start_date + timedelta(days=i) for i in range(delta)]
