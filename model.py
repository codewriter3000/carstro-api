import psycopg2
import sys
from dotenv import dotenv_values

def connect():
    config = dotenv_values('.env')

    return psycopg2.connect(dbname=config['DB_NAME'], user=config['DB_USER'], password=config['DB_PASS'], host=config['DB_HOST'], port=config['DB_PORT'])

def migrate():
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE users (id serial PRIMARY KEY, username VARCHAR(20), password_digest CHAR(64), password_salt VARCHAR(8), first_name VARCHAR(16), last_name VARCHAR(16));')
    cursor.execute('CREATE TABLE roles (id serial PRIMARY KEY, name VARCHAR(32), authority SMALLINT, is_admin BOOLEAN);')
    cursor.execute('CREATE TABLE user_role (user_id INTEGER REFERENCES users(id), role_id INTEGER REFERENCES roles(id), PRIMARY KEY (user_id, role_id));')
    
    conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    if sys.argv[1] == 'migrate':
        migrate()

