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
    
    def get_hydrometers_with_predictions(self, days):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT h.id, h.code, h.name, p.value, p.date, 
            COALESCE(
                (SELECT value FROM predictions WHERE hydrometer_id = h.id AND date = date('now', '-{} day')),
                (SELECT value FROM predictions WHERE hydrometer_id = h.id AND date < date('now', '-{} day') ORDER BY date DESC LIMIT 1)
            ) AS previous_value
            FROM hydrometers h
            JOIN predictions p ON h.id = p.hydrometer_id
            WHERE p.date = (SELECT MAX(date) FROM predictions WHERE hydrometer_id = h.id)
            ORDER BY h.name, p.date
        '''.format(days, days))

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

    def get_hydrometers_with_predictions2(self, days):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id
            FROM hydrometers
            ORDER BY name       
        ''')

        results = cursor.fetchall()

        values = []
        for e in results:
            values.append(e[0])

        # Cria uma lista vazia para armazenar os resultados
        output = []

        # Usa um loop for para iterar sobre a lista de valores
        for value in values:
            # Executa a consulta SQL com a substituição de parâmetros
            cursor.execute('''
                SELECT SUM(CAST(value AS INTEGER)) AS water_consumption 
                FROM predictions WHERE hydrometer_id = ? 
                AND date BETWEEN DATE('now', 'start of day', '-' || ? || ' days') 
                AND DATE('now', 'start of day')
            ''', (value, days)) # Substitui os ? pelo valor de hydrometer_id e o número de dias
            
            # Obtém o resultado da consulta
            result = cursor.fetchone()

            # Adiciona uma tupla com o hydrometer_id e o water_consumption à lista de saída
            output.append((value, result[0]))

        # Fecha a conexão
        conn.close()

        # Retorna a lista de saída
        return output


