import sqlite3
import os

import scraper

TABLE_FILE_NAME = "advantages.db"

class DatabaseWriter:

    c = None
    conn = None

    def __init__(self, results):
        self.create_table()
        self.add_hero_names(results)
        self.add_advantages(results)
        self.save_table()

    def create_table(self):
        # ensure we delete the existing file, if it exists
        if(os.path.isfile(TABLE_FILE_NAME)):
            os.remove(TABLE_FILE_NAME)

        self.conn = sqlite3.connect(TABLE_FILE_NAME)
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE Names (
                         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                         name TEXT)""")
        self.c.execute("""CREATE TABLE Advantages (
                         hero_id INTEGER,
                         enemy_id INTEGER,
                         advantage DECIMAL(2,2))""")

    def add_hero_names(self, results):
        for item in results:
            self.c.execute("INSERT INTO Names (name) VALUES ('{}')".format(item.name))

    def add_advantages(self, results):
        for data_for_a_hero in results:
            self.c.execute("SELECT id FROM Names WHERE name='{}';".format(data_for_a_hero.name))
            hero_id = self.c.fetchone()[0]
            for item in data_for_a_hero.data:
                self.c.execute("SELECT id FROM Names WHERE name='{}';".format(item.name))
                enemy_id = self.c.fetchone()[0]
                self.c.execute("INSERT INTO Advantages (hero_id, enemy_id, advantage) VALUES ({}, {}, {})".format(hero_id, enemy_id, item.advantage))


    def save_table(self):
        self.conn.commit()
        self.conn.close()

