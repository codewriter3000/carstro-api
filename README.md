# Carstro API
## Brief Description
I am trying to build a basic boilerplate app for an admin panel. The front-end that goes along with this can be found here: https://github.com/codewriter3000/carstro
## API Tech Stack
- Python FastAPI: API library
- PostgreSQL: Database
- Psycopg2: Postgres driver library
## How to Setup
1. Run `git clone https://github.com/codewriter3000/carstro-api`
2. Run `python -m venv ./venv`
3. Run `pip install -r requirements.txt`
4. Create a `.env` file
5. Make sure you have the following environment variables:
   - DB_NAME
   - DB_HOST
   - DB_USER
   - DB_PASS
   - DB_PORT
   - SECRET_KEY
6. Run `cd app` then `python model.py migrate`
7. To run this API back-end, go into the project root and run `fastapi dev main.py`
