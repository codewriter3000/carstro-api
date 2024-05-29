import psycopg2
import sys
from dotenv import dotenv_values


def connect():
    config = dotenv_values('.env')
    return psycopg2.connect(dbname=config['DB_NAME'], user=config['DB_USER'], password=config['DB_PASS'], host=config['DB_HOST'], port=config['DB_PORT'])


def migrate():
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE users (id serial PRIMARY KEY, username VARCHAR(20), '
                   'password_digest VARCHAR(100), password_salt VARCHAR(16), first_name VARCHAR(16), '
                   'last_name VARCHAR(16), is_admin BOOLEAN DEFAULT FALSE, is_enabled BOOLEAN DEFAULT TRUE);')
    cursor.execute('CREATE TABLE roles (id serial PRIMARY KEY, name VARCHAR(32), authority SMALLINT, is_admin BOOLEAN);')
    cursor.execute('CREATE TABLE user_role (user_id INTEGER REFERENCES users(id), role_id INTEGER REFERENCES roles(id), PRIMARY KEY (user_id, role_id));')
    cursor.execute('CREATE TABLE jwts (token VARCHAR(120), expiration TIMESTAMP, is_valid BOOLEAN DEFAULT TRUE);')
    cursor.execute(r"""
    -- Step 1: Create the function
CREATE OR REPLACE FUNCTION delete_invalid_jwt()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the is_valid column is false
    IF NEW.is_valid = FALSE THEN
        DELETE FROM jwts WHERE token = NEW.token;
        RETURN NULL; -- Return NULL to skip the operation as the record is deleted
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 2: Create the trigger
CREATE TRIGGER jwt_before_update_insert
BEFORE INSERT OR UPDATE ON jwts
FOR EACH ROW
EXECUTE FUNCTION delete_invalid_jwt();
    """)

    conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    if sys.argv[1] == 'migrate':
        print('Migration beginning')
        migrate()
