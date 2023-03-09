import datetime
import sqlite3

conn = sqlite3.connect('HundeOplevelser.db')


class FoodDispenserRepository:

    def EnsureCreated(self):
        sql = '''
                    CREATE TABLE IF NOT EXISTS FOOD_DISPENSED_AT_TIME (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT NOT NULL
                    )
                    '''
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()

    def saveData(self, date):
        global conn
        sql = 'INSERT INTO FOOD_DISPENSED_AT_TIME (topic) VALUES (?)'
        dateString = date.strftime("%m/%d/%Y, %H:%M:%S")
        cursor = conn.cursor()
        cursor.execute(sql, [dateString])
        conn.commit()
        cursor.close()

