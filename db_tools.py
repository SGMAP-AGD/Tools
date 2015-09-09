# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:10:23 2015

@author: Florian
"""
from sqlalchemy import create_engine
import psycopg2

# cfg
from Tools.config import *

##############
# PostgreSQL #
##############


# -- Connect
def connect(schema, table_name):
    ''' connexion postgre à partir d'un tuple (schema, table) et renvoie un tuple (table, colnames)'''
    conn_string = "host='" + ipserver + "' dbname='" + dbname + "' user='" + user + "' password='" + password + "' client_encoding='utf-8' "
    # print the connection string we will use to connect
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    print("Connected!")
    command = "SELECT * FROM " + schema + "." + table_name
    cur.execute(command)
    colnames = [desc[0] for desc in cur.description]
    return (cur.fetchall(), colnames)


# -- Create table
def create_table(df, table_name, schema):
    engine = create_engine(r'postgresql://' + user + ':' + password + '@' + ipserver + '/' + user, encoding='utf-8')
    try:
        df.to_sql(table_name, engine, schema=schema)
        print("Table créée")
    except ValueError:
        print("Table already exists")
        pass
