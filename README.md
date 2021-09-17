# Airport

Instructions on how to run the project:
  - clone the project
  - install: 
    - bs4 (pip install beautifulsoup4)
    - urllib (pip install urllib3)
    - requests (pip install requests)
    - selenium (pip install selenium)
    - webdriver_manager (pip install webdriver-manager)
  - run the main.py file (Airport/venv/Include/main.py)
  - the result is printed in console (time, city, city temperature and note for each of the flights)

If you want to see how caching is working, you have to uncomment the following lines:
  - createCache(times, cities, temperatures)
  - json_data = readCache()
  - notes = createNotesFromJson(json_data)
  - print(notes)

If you want to run the tests:
  - run test.py (Airport/venv/Include/test.py)
 
 
