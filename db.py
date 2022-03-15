from sqlite3 import Cursor
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

CREATE_TRANSACTION_TABLE = '''
CREATE TABLE IF NOT EXISTS transaction
(id SERIAL PRIMARY KEY, coinbase_id TEXT UNIQUE, transaction_type TEXT, transaction_value DECIMAL, transaction_date TEXT);
'''
INSERT_TRANSACTION = '''
INSERT INTO transaction (coinbase_id,transaction_type,transaction_value,transaction_date) 
VALUES (%s,%s,%s,%s); 
'''
SELECT_COINBASE_ID = '''
SELECT coinbase_id FROM transaction;
'''
SELECT_TRANSACTIONS = '''
SELECT * FROM transaction;
'''

def connect():
    try:
        conn = psycopg2.connect(
            user ='postgres',
            password=os.getenv('DB_PASSWORD'),
            host='localhost',
            database='coinbase-tracker'
        )
    except ConnectionError as exc:
        raise RuntimeError('Failed to open database') from exc

    return conn


def create_table(conn): 
    with conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_TRANSACTION_TABLE)
        cursor.close()


def add_transaction(conn,coinbase_id,transaction_type,transaction_value,transaction_date):
    with conn:
        cursor = conn.cursor()
        cursor.execute(INSERT_TRANSACTION, (coinbase_id,transaction_type,transaction_value,transaction_date))
        cursor.close()


def get_coinbase_ids(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_COINBASE_ID)
        result = cursor.fetchall()
        cursor.close()
        return result


def get_transactions(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_TRANSACTIONS)
        result = cursor.fetchall()
        cursor.close()
        return result