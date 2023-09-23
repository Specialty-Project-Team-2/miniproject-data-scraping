import time
from selenium.webdriver.chrome.webdriver import WebDriver

from util.file_handler import saveAsFile, make_file_path

from collections import deque
from time import sleep

from random import uniform


def scroll_until_limit(driver : WebDriver, max_num = 500, unit_scroll_height = 1000000, pause_time=1, patience=5):
    javascript_scroll_down = f"window.scrollTo(0, window.pageYOffset + {unit_scroll_height})"
    javascript_get_page_y_offset = "return window.pageYOffset"

    cnt = 0
    pageYOffset = None
    que = deque([None] * patience, maxlen=patience)
    while cnt < max_num and pageYOffset != (new_offset := driver.execute_script(javascript_get_page_y_offset)):
        driver.execute_script(javascript_scroll_down)
        
        que.append(new_offset)
        pageYOffset, cnt = que[0], cnt+1
        
        print(f"{cnt}번째 높이: {pageYOffset}")
        print(que)
        print()
        
        time.sleep(pause_time)
        
def scroll_down(driver : WebDriver, unit_scroll_height = 1000000):
    javascript_scroll_down = f"window.scrollTo(0, window.pageYOffset + {unit_scroll_height})"

    driver.execute_script(javascript_scroll_down)

def is_element_in_window(driver : WebDriver, css_selector):
    query_js = f"""
        var element = document.querySelector("{css_selector}")
        if(!element) return false;
        
        var rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    """
    return driver.execute_script(query_js)

def scroll_until_lender_of(driver : WebDriver, css_selector, total_sec=500, unit_sec=10, total_scroll_sec=5):
    skip_time_unit = unit_sec / total_sec * total_scroll_sec
    
    for i in range(0, total_sec, unit_sec):
        if is_element_in_window(driver, css_selector): break
        
        scroll_down(driver, i)
        sleep(skip_time_unit)
        
def save_html_as(driver : WebDriver, file_name):
    file_path = make_file_path(file_name)
    saveAsFile(file_path, driver.page_source)

def sleep_like_human():
    sleep(uniform(3, 5))