import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

conn_str = os.getenv('TEST_PGSQL_CONNECTION')

if not conn_str:
    raise ValueError('TEST_PGSQL_CONNECTION not set in .env')

sql_file = 'social_network_schema.sql'

with open(sql_file, 'r') as f:
    sql = f.read()

# Connect and execute
try:
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    print('Schema and sample data loaded successfully.')
except Exception as e:
    print('Error:', e) 