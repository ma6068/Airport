from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import db
import os


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

def getTemperature(cities):
    api_key = 'b8dffc5cce80c763531d05464a0f37e0'
    temperatures = []
    for city in cities:
        apiUrl = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api_key
        try:
            json_data = requests.get(apiUrl).json()
            temperature = (int)(json_data['main']['temp'] - 273.15)  # from kelvin to celsius
        except:
            temperature = 'No info'  # no temperature info for that city
        temperatures.append(temperature)
    return temperatures

def getNotes(temperatures, cities):
    notes = []
    for i in range(len(temperatures)):
        # if there is no info for temperature
        if temperatures[i] == 'No info':
            note = 'No temperature information'
        # Spain
        elif (cities[i] == 'Barcelona' or cities[i] == 'Madrid') and temperatures[i] >= 22:
            note = 'Hace mucho calor.'
        elif (cities[i] == 'Barcelona' or cities[i] == 'Madrid') and temperatures[i] < 22:
            note = 'No hace mucho calor.'
        # Germany
        elif (cities[i] =='Frankfurt' or cities[i] == 'Stuttgart' or cities[i] == 'Leipzig') and temperatures[i] >= 22:
            note = 'Es ist sehr heiß.'
        elif ( cities[i] =='Frankfurt' or cities[i] == 'Stuttgart' or cities[i] == 'Leipzig') and temperatures[i] < 22:
            note = 'Es ist nicht sehr heiß.'
        # Other
        elif temperatures[i] >= 22:
            note = 'It\'s very hot.'
        else:
            note = 'It is not very hot.'
        notes.append(note)
    return notes

if __name__ == "__main__":
    url = 'https://www.viennaairport.com/passagiere/ankunft__abflug/abfluege'
    times, cities = getCityAndTime(url)
    temperatures = getTemperature(cities)
    notes = getNotes(temperatures, cities)
    try:
        os.remove('airport.db')
    except:
        print('File does not exist.')
    db = db.DB()
    db.createTable()
    for i in range(len(times)):
        db.insert_airport(times[i], cities[i], temperatures[i], notes[i])
    # print(db.get_all_airports())


