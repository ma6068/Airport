import sqlite3

class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connectDB()

    def connectDB(self):
        if self.conn is None:
            try:
                self.conn = sqlite3.connect('airport.db')
                self.cur = self.conn.cursor()
            except sqlite3.Error as error:
                print(error)

    def disconnectDB(self):
        if self.conn:
            self.conn.close()
        if self.cur:
            self.cur.close()

    def createTable(self):
        self.cur.execute('''
            CREATE TABLE Airport (
                id INTEGER NOT NULL PRIMARY KEY,
                time TEXT NOT NULL,
                city TEXT NOT NULL,
                temperature INTEGER,
                note TEXT
                );
        ''')
        self.conn.commit()

    # ------------------------------  POST ------------------------------
    def insert_airport(self, time, city, temperature, note):
        try:
            self.cur.execute("INSERT INTO Airport(time, city, temperature, note)"
                             "VALUES (?, ?, ?, ?)", (time, city, temperature, note))
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()

    # ------------------------------ GET ------------------------------
    def get_all_airports(self):
        try:
            self.cur.execute("SELECT * FROM Airport",)
            posting = self.cur.fetchall()
            if posting:
                return posting
            return None
        except sqlite3.Error:
            self.conn.rollback()
            return None