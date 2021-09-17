from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import db
import os
import json


def getCityAndTime(url):
    try:
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
    except:
        print('Something went wrong')

def getTemperature(cities):
    try:
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
    except:
        print('Something went wrong')

def createNotes(temperatures, cities):
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

def createCache(times, cities, temperatures):
    try:
        os.remove('cache_data.txt')
    except:
        pass
    data_set = {}
    for i in range(len(times)):
        data_set['key_' + str(i)] = (times[i], cities[i], temperatures[i])
    with open('cache_data.txt', 'w') as outfile:
        json.dump(data_set, outfile, ensure_ascii=False)

def readCache():
    with open('cache_data.txt') as json_file:
        data_set = json.load(json_file)
        return data_set

def createNotesFromJson(json_data):
    cities = []
    temperatures = []
    for key in json_data:
        cities.append(json_data[key][1])
        temperatures.append(json_data[key][2])
    return createNotes(temperatures, cities)


def test3(times, cities):
    for i in range(len(times)):
        if not times[i] or not cities[i]:
            return False
    return True

if __name__ == "__main__":
    url = 'https://www.viennaairport.com/passagiere/ankunft__abflug/abfluege'
    times, cities = getCityAndTime(url)
    temperatures = getTemperature(cities)
    notes = createNotes(temperatures, cities)

    #################################### Put data in database ####################################
    try:
        os.remove('airport.db')
    except:
        pass
    db = db.DB()
    db.createTable()
    for i in range(len(times)):
        db.insert_airport(times[i], cities[i], temperatures[i], notes[i])
    print(db.get_all_airports())

    #################################### Caching ####################################
    # createCache(times, cities, temperatures)
    # json_data = readCache()
    # notes = createNotesFromJson(json_data)
    # print(notes)

    #################################### Test ####################################
    # check if we get the time and cities (they are not null)
    # if test3(times, cities): print('OK')