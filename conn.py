import json

import sqlalchemy as sa

CONFIG_FILE = 'config.json'

def load_config() -> dict:   
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_connection(config: dict) -> sa.Engine:
    url_object = sa.URL.create(
        drivername=config['drivername'],
        host=config['host'],
        username=config['username'],
        password=config['password'],
        database=config['database'],
    )
    engine = sa.create_engine(url_object)
    return engine
