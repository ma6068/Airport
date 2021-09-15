from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re


def getCityAndTime(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    html_code = soup.prettify()
    # get the times
    times = re.findall("<div class=\"detail-table__cell text-center fdabf-td1\">([^<]*)</div>", html_code)
    for i in range(len(times)):
        times[i] = times[i].strip()   # delete empty spaces in string
    times.pop()  # last element is not a time => delete it
    # get the cities
    cities = re.findall("<span class=\"visible-xs\">([^<]*)</span>", html_code)
    for i in range(len(cities)):
        cities[i] = cities[i].strip()  # delete empty spaces in string
    cities = cities[: len(cities) - 2] # last two elements are not a city => delete it
    return times, cities

if __name__ == "__main__":
    url = 'https://www.viennaairport.com/passagiere/ankunft__abflug/abfluege'
    times, cities = getCityAndTime(url)
