import time
from selenium.webdriver.chrome.webdriver import WebDriver

from util.file_handler import saveAsFile, make_file_path

from collections import deque


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
        
def save_html_as(driver : WebDriver, file_name):
    file_path = make_file_path(file_name)
    saveAsFile(file_path, driver.page_source)