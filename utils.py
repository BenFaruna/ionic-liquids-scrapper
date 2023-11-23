#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Dict

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By


def enter_search_query(driver: webdriver, query: int) -> None:
    """opens the search bar and searches for the query"""

    print("Started for query", query)

    option = f"#dijit_MenuItem_{query}_text"

    button = driver.find_element(By.CSS_SELECTOR, "#sbutton_label")
    submit_button = driver.find_element(By.CSS_SELECTOR, "#submbutt_label")

    button.click()

    driver.find_element(By.CSS_SELECTOR, "#resetbutt_label").click()

    dropdown_input = driver.find_element(By.CSS_SELECTOR, "#ncmp > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)")
    dropdown_input.click()

    dropdown_option = driver.find_element(By.CSS_SELECTOR, option)
    dropdown_option.click()

    submit_button.click()


def get_table_data(driver) -> List[Dict]:
    data = []
    data_tables = driver.find_elements(By.CSS_SELECTOR, "table.dgrid-row-table")

    for table in data_tables[1:]:
        data.append(extract_table_data(table))
    
    return data


def extract_table_data(webelement) -> dict:
    row_data = {}

    headers = [
        "SetID", "Reference", "Property", "Phase(s)",
        "Component 1", "Component 2", "Component 3",
        "Datapoints", "Name 1", "Name 2", "Name 3"
    ]

    soup = BeautifulSoup(webelement.get_attribute("outerHTML"), "lxml")
    data = soup.find_all("td", attrs={"role": "gridcell"})

    for i, header in enumerate(headers):
        if header.startswith("Component"):
            try:
                row_data[header] = "https://ilthermo.boulder.nist.gov" + data[i].img.get("src")
            except AttributeError:
                row_data[header] = ""
        else:
            if header == "Phase(s)":
                phase = [li.text for li in data[i].find_all("li")]
                row_data[header] = ";".join(phase)
            else:
                row_data[header] = data[i].text

    return row_data

