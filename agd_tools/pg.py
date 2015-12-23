#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions to interface postgresql and pandas.

import_df() imports a pandas Dataframe from a PostgreSQL table.
export_df() exports a pandas Dataframe from a PostgreSQL table.
"""

import configparser
import os
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

__author__ = "Florian, Paul, Michel"

# Read config file
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")
config_host = config["PostgreSQL"]["host"]
config_dbname = config["PostgreSQL"]["dbname"]
config_user = config["PostgreSQL"]["user"]
config_schema = config["PostgreSQL"]["schema"]


def get_conn_string(host, dbname, user, password="", client_encoding="utf-8"):
    """Private function. Construct a postgresql connection string.
    """
    conn_string = "host='" + host + "' " + \
                  "dbname='" + dbname + "' " + \
                  "user='" + user + "' " + \
                  "password='" + password + "' " + \
                  "client_encoding='" + client_encoding + "'"
    return conn_string


def get_engine(host, dbname, user, password="", port=5432,
               client_encoding="utf-8"):
    """Private function. Return a sqlalchemy engine.
    """
    conn_string = "postgresql://" + user + ":" + password + "@" + \
                  host + ":" + str(port) + "/" + dbname
    return create_engine(conn_string, client_encoding=client_encoding)


def execute_sql(sql, commit=False):
    """Execute sql code using PostgreSQL parameters in the config file.

    This is a private function.

    :param sql: SQL script to execute
    :type sql: string
    :return: A dataframe or nothing
    :rtype: pandas.DataFrame
    """
    conn_string = get_conn_string(host=config_host,
                                  dbname=config_dbname,
                                  user=config_user)
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute(sql)
    if (isinstance(cur.description, type(None)) is False):
        # Some commands do not return rows. Ex: DROP, CREATE...
        colnames = [col[0] for col in cur.description]
        df = pd.DataFrame(cur.fetchall(), columns=colnames)
        cur.close()
        if(commit):
            conn.commit()
        return(df)
    else:
        cur.close()
        if(commit):
            conn.commit()


def export_df(df, table_name, schema=None, if_exists='fail'):
    """Export a pandas Dataframe to a PostgreSQL table."""

    if not schema:
        schema = config_schema

    engine = get_engine(host=config_host,
                        dbname=config_dbname,
                        user=config_user)

    return df.to_sql(table_name, engine, schema=schema, if_exists=if_exists)


def import_df(table_name, schema=None):
    """Import a pandas Dataframe from a PostgreSQL table."""

    if not schema:
        schema = config_schema

    sql = "SELECT * FROM " + schema + "." + table_name

    return execute_sql(sql)
