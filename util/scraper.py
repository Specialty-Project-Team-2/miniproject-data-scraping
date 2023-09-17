from selenium import webdriver
from config.chrome_option import options, service

from selenium.webdriver.chrome.webdriver import WebDriver

from typing import Callable


def scrap(execute_plan : Callable[[WebDriver], None]) -> None:
    with webdriver.Chrome(service=service, options=options) as driver:
        execute_plan(driver)