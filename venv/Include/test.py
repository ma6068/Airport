import db
import json

try:
    os.delete('airport.db')
except:
    pass

db = db.DB()
db.createTable()

def readCache():
    with open('cache_data.txt') as json_file:
        data_set = json.load(json_file)
        return data_set

def createNote(city, temperature):
    note = ''
    # if there is no info for temperature
    if temperature == 'No info':
        note = 'No temperature information'
    # Spain
    elif (city == 'Barcelona' or city == 'Madrid') and temperature >= 22:
        note = 'Hace mucho calor.'
    elif (city == 'Barcelona' or city == 'Madrid') and temperature < 22:
        note = 'No hace mucho calor.'
    # Germany
    elif (city == 'Frankfurt' or city == 'Stuttgart' or city == 'Leipzig') and temperature >= 22:
        note = 'Es ist sehr heiß.'
    elif (city == 'Frankfurt' or city == 'Stuttgart' or city == 'Leipzig') and temperature < 22:
        note = 'Es ist nicht sehr heiß.'
    # Other
    elif temperature >= 22:
        note = 'It\'s very hot.'
    else:
        note = 'It is not very hot.'
    return note

# check if inserting in database is ok
def test1():
    db.insert_airport('12:30', 'Mardir', '23', 'So cool!!!')
    result = db.get_all_airports()
    if ('12:30', 'Mardir', 23, 'So cool!!!') in result:
        return True
    return False

# check if note in database and cached note are the same
def test2():
    result = db.get_all_airports()
    ok_list = []
    for i in range(len(result)):
        time, city, temperature, note1 = result[0]
        json_data = readCache()
        for key in json_data:
            if json_data[key][1] == city and json_data[key][2] == temperature:
                note2 = createNote(city, temperature)
                if note1 == note2:
                    ok_list.append(True)
                else:
                    ok_list.append(False)
    if False in ok_list:
        return False
    return True


if (test1()): print('OK')
if (test2()): print('OK')  # for this test we need files db.py and cache_data.txt
