import db

try:
    os.delete('airport.db')
except:
    pass

db = db.DB()
db.createTable()
db.insert_airport('12:30', 'Mardir', '23', 'So cool!!!')
result = db.get_all_airports()
if ('12:30', 'Mardir', 23, 'So cool!!!') in result:
    print('Ok')