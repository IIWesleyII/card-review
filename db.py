import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
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
SELECT * FROM transaction
WHERE transaction_date between %s AND %s
;
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


def select_coinbase_ids(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_COINBASE_ID)
        result = cursor.fetchall()
        cursor.close()
        return result


def select_transactions(conn,time_period):
    with conn:
        cursor = conn.cursor()
        curr_date = datetime.today()
        # date_1 is the current date minus the time_period in days  
        date_1 = str(curr_date + timedelta(days=-time_period))

        # date_2 is current time date
        date_2 =str(curr_date) 

        cursor.execute(SELECT_TRANSACTIONS,(date_1,date_2))
        result = cursor.fetchall()
        cursor.close()
        return result 