# Handles PostgreSQL DB initialization

import configparser

import os
import psycopg2

# Get DB config
db_config = configparser.ConfigParser()
db_config.read(os.path.join(
    os.path.join(os.path.abspath(os.path.dirname(__file__)),
                 'config/config.ini')))
db_server = db_config['DEFAULT']['db.server']
db_port = db_config['DEFAULT']['db.port']
db_name = db_config['DEFAULT']['db.name']
db_user = db_config['DEFAULT']['db.user']
db_password = db_config['DEFAULT']['db.password']

conn = psycopg2.connect(
    f"dbname='{db_name}' user='{db_user}' host='{db_server}' port='{db_port}' password='{db_password}'")
