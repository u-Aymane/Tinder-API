import os
import sqlite3
from tinderapi import TinderProfile


class TinderDB:
    def __init__(self, scavenger=False):
        self.connection = None
        self.db = 'Tinder.db'
        self.table = 'tinder'
        if not scavenger:
            self.matches = []
            if not os.path.exists('Tinder.db'):
                self.create_table()

        self.rows = None

    def connect(self):
        self.connection = sqlite3.connect(self.db)

    def create_table(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"""CREATE TABLE {self.table} (
                    id TEXT,
                    verified INTEGER,
                    bio TEXT,
                    birth_date TEXT,
                    name TEXT,
                    photos TEXT,
                    gender INTEGER,
                    city TEXT,
                    show_gender_on_profile INTEGER,
                    recently_active INTEGER,
                    online_now INTEGER,
                    distance_mi REAL,
                    distance_km REAL,
                    s_number INTEGER,
                    teaser TEXT,
                    match INTEGER,
                    like INTEGER DEFAULT 0
        
        )""")

        self.connection.close()

    def execute_query(self, query: str):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query)
            if 'select' in query.lower():
                self.rows = cursor.fetchall()
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            with open('tinder.log', 'a', encoding='utf-8') as f:
                f.writelines(f'exception: {e}\nquery: {query}\n')
            f.close()
            print(f'error: query')

    def insert_into_table(self, profileData: TinderProfile):
        QUERY = f"""INSERT INTO {self.table} VALUES (
                        '{profileData.id}',
                        {1 if profileData.verified else 0},
                        "{profileData.bio}",
                        '{profileData.birth_date}',
                        '{profileData.name}',
                        '{','.join(profileData.photos)}',
                        {profileData.gender},
                        "{profileData.city}",
                        {1 if profileData.show_gender_on_profile else 0},
                        {1 if profileData.recently_active else 0},
                        {1 if profileData.online_now else 0},
                        {profileData.distance_mi},
                        {profileData.distance_km},
                        {profileData.s_number},
                        "{profileData.teaser}",
                        {1 if profileData.match else 0},
                        0
                
        )"""

        self.execute_query(QUERY)

    def select_from_table(self, profileData: TinderProfile):
        QUERY = f"""SELECT * FROM {self.table} WHERE id='{profileData.id}'"""
        self.execute_query(QUERY)
        return self.rows

    def select_from_table_simple_id(self, profileData, like_option=False):
        QUERY = f"""SELECT * FROM {self.table} WHERE id='{profileData}'"""
        if like_option:
            QUERY += ' AND like = 0'
        self.execute_query(QUERY)
        return self.rows

    def setLike(self, profile_id):
        QUERY = f"""UPDATE {self.table} SET like=1 WHERE id='{profile_id}'"""
        self.execute_query(QUERY)

    def setDislike(self, profile_id):
        QUERY = f"""UPDATE {self.table} SET like=-1 WHERE id='{profile_id}'"""
        self.execute_query(QUERY)
