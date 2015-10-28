# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:10:23 2015

@author Florian
@author boupetch
"""

from sqlalchemy import create_engine
import psycopg2
import paramiko
import pandas as pd
import configparser

# Read config file
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
    # Some commands do not return rows. Ex: DROP, CREATE...
    if (isinstance(cur.description, type(None)) == False):
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

#######
# SSH #
#######


def connect_sftp_csv(rep, csv):
    ''' crée une connexion sftp sur le server secure et permet notamment
    l'accès à des fichiers contenus sur le server'''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(config.ipsecure, username=config.user, password='')
    except paramiko.SSHException:
        print("Connection Error")

    sftp = ssh.open_sftp()
    sftp.chdir(rep)
    table = pd.read_csv(sftp.open(csv))
    ssh.close()
    return table

    # USE #
    # sftp.chdir("/var/data/stsisi/")
    # sftp.open('iris60.csv')
    # ssh.close()
