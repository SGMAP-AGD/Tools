# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:10:23 2015

@author: Florian
"""

import getpass
from sqlalchemy import create_engine
import psycopg2

# cfg
import Tools.config as config

##############
# PostgreSQL #
##############


# -- Connect
def connect(schema, table_name):
    ''' connexion postgre à partir d'un tuple (schema, table) et renvoie un tuple (table, colnames)'''
    password = getpass.getpass("Entrez le mot de passe du server : ")
    dbname = input("Par défaut, la base chargée est celle de config, entrez" + \
                    " un autre nom si vous voulez, sinon, touche entrée")
    if dbname == '':
        dbname = config.dbname

    conn_string = "host='" + config.ipserver + "' dbname='" + dbname + \
                   "' user='" + config.user + "' password='" + password + \
                   "' client_encoding='utf-8' "
    # print the connection string we will use to connect
    conn = psycopg2.connect(conn_string)
    del password, conn_string
    cur = conn.cursor()
    print("Connected!")
    command = "SELECT * FROM " + schema + "." + table_name
    cur.execute(command)
    colnames = [desc[0] for desc in cur.description]
    return (cur.fetchall(), colnames)


# -- Create table
def create_table(df, table_name, schema):
    password = getpass.getpass("Entrez le mot de passe du server : ")

    conn_string = r'postgresql://' + config.user + ':' + password + '@' + \
        config.ipserver + '/' + config.user
    engine = create_engine(conn_string, encoding='utf-8')

    del password, conn_string

    try:
        df.to_sql(table_name, engine, schema=schema)
        print("Table créée")
    except ValueError:
        print("Table already exists")
        pass
