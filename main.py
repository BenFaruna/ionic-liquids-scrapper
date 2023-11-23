#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import threading

from queue import Queue

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from webdriver_manager.firefox import GeckoDriverManager

from utils import enter_search_query, get_table_data
from csv_utils import thread_function


data_queue = Queue()
data_thread = threading.Thread(name="data_thread", target=thread_function, args=(data_queue,))
data_thread.start()


_options = webdriver.FirefoxOptions()
_options.add_argument('--headless')
_options.add_argument('--no-sandbox')
_options.add_argument('--disable-dev-sh-usage')


driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=_options)
driver.get("https://ilthermo.boulder.nist.gov")

wait = WebDriverWait(driver, 200)

wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#sbutton_label")))


for i in range(2, 5):
    enter_search_query(driver, i)

    wait.until_not(ec.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[1]")))

    next_btn = driver.find_element(By.CSS_SELECTOR, ".dgrid-next")

    while True:
        # print(next_btn.get_attribute("tabindex"))
        data = get_table_data(driver)
        data_queue.put(data)

        if next_btn.get_attribute("tabindex") == "-1":
            break

        next_btn.click()
        time.sleep(0.2)
else:
    data_queue.put([])


driver.close()
