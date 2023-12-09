# database.py
import sqlite3
from datetime import datetime, timedelta
import random
from faker import Faker

class BancoDeDados:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connect()
        self.create_table()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hydrometers (
                id INTEGER PRIMARY KEY, 
                code TEXT NOT NULL UNIQUE,
                name TEXT       
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY, 
                value TEXT NOT NULL, 
                date TEXT NOT NULL, 
                hydrometer_id INTEGER,
                FOREIGN KEY(hydrometer_id) REFERENCES hydrometers(id)
            )
        ''')
        conn.commit()
        conn.close()

    def config_database(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        conn.commit()
        conn.close()

    def insert(self, code, value, name=None, date=None):

        if date is None:
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')

        if name is None:
            name = "Nao definido"

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO hydrometers(code, name) VALUES(?, ?)', (code, name))
        cursor.execute('SELECT id FROM hydrometers WHERE code = ?', (code,))

        hydrometer_id = cursor.fetchone()[0]

        cursor.execute(
            'INSERT INTO predictions(value, date, hydrometer_id) VALUES(?, ?, ?)', 
            (value, date, hydrometer_id)
        )

        conn.commit()
        conn.close()

    def search_recent(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT predictions.*, hydrometers.code, hydrometers.name
            FROM predictions
            INNER JOIN hydrometers ON predictions.hydrometer_id = hydrometers.id
            ORDER BY date DESC
            LIMIT 10
        ''')
        results = cursor.fetchall()
        conn.close()
        return results
   
    def populate_database(self, num_hidrometros, num_predicoes):
        fake = Faker()
        for _ in range(num_hidrometros):
            code = str(random.randint(1000, 99999))
            name = fake.name()

            for _ in range(num_predicoes):
                value = str(random.randint(1000000, 9999999))
                date = datetime.now() - timedelta(days=random.randint(0, 365))
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                self.insert(code, value, name, date)

    def get_hydrometers_with_predictions(self, days):
        hydrometers_predictions = {}

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name
            FROM hydrometers
            ORDER BY name       
        ''')
        results_hydrometers = cursor.fetchall()

        for hydrometer in results_hydrometers:
            params = {'hydrometer_id': hydrometer[0], 'day': days}
            
            # Encontrar o valor da previsão mais antiga
            cursor.execute('''
                SELECT value
                FROM predictions
                WHERE 
                    hydrometer_id = :hydrometer_id AND
                    date = (
                        SELECT MIN(date)
                        FROM predictions
                        WHERE 
                            hydrometer_id = :hydrometer_id AND
                            date >= datetime('now', '-' || :day || ' day')
                    )
            ''', params)
            oldest_result = cursor.fetchone()
            oldest_value = oldest_result[0] if oldest_result is not None else '0000000'

            params['oldest_date'] = oldest_value

            # Encontrar o valor da previsão mais recente que esteja entre a data mais antiga e a data atual
            cursor.execute('''
                SELECT value
                FROM predictions
                WHERE 
                    hydrometer_id = :hydrometer_id AND
                    date = (
                        SELECT MAX(date)
                        FROM predictions
                        WHERE 
                            hydrometer_id = :hydrometer_id AND
                            date > :oldest_date AND
                            date <= datetime('now')
                    )
            ''', params)
            newest_result = cursor.fetchone()
            newest_value = newest_result[0] if newest_result is not None and oldest_result is not None  else '0000000'

            hydrometers_predictions[hydrometer[1]] = {
                "oldestValue": oldest_value,
                "newestValue": newest_value
            }

        return hydrometers_predictions


