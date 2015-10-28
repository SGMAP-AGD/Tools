#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import configparser

__author__ = "Florian, Paul"

""" Read config file """
config = configparser.ConfigParser()
config.read("config.ini")


def get_conn_string(host, dbname, user, password="", client_encoding="utf-8"):
    conn_string = "host='" + host + "' " + \
                  "dbname='" + dbname + "' " + \
                  "user='" + user + "' " + \
                  "password='" + password + "' " + \
                  "client_encoding='" + client_encoding + "'"
    return conn_string


def get_engine(host, dbname, user, password="", port=5432,
               client_encoding="utf-8"):
    conn_string = "postgresql://" + user + ":" + password + "@" + \
                host + ":" + str(port) + "/" + dbname
    return create_engine(conn_string, client_encoding=client_encoding)


def export_df(df, table_name, schema="public", if_exists='fail'):
    engine = get_engine(host=config["PostgreSQL"]["host"],
                        dbname=config["PostgreSQL"]["dbname"],
                        user=config["PostgreSQL"]["user"])
    return df.to_sql(table_name, engine, schema=schema, if_exists=if_exists)


def execute_sql(sql):
    conn_string = get_conn_string(host=config["PostgreSQL"]["host"],
                                  dbname=config["PostgreSQL"]["dbname"],
                                  user=config["PostgreSQL"]["user"])
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute(sql)
    if (isinstance(cur.description, type(None)) == False):
        """ Some commands do not return rows. Ex: DROP, CREATE... """
        colnames = [col[0] for col in cur.description]
        rows = pd.DataFrame(cur.fetchall())
        cur.close()
        conn.commit()
        return (rows, colnames)
    else:
        cur.close()
        conn.commit()


def import_table(table_name, schema="public"):
    sql = "SELECT * FROM " + schema + "." + table_name
    return execute_sql(sql)


