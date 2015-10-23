# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:10:23 2015

@author: Florian
"""

from sqlalchemy import create_engine
import psycopg2
import paramiko
import pandas as pd
# cfg
import config as config

##############
# PostgreSQL #
##############


# -- Connect
def connect(schema, table_name):
    ''' connexion postgre à partir d'un tuple (schema, table)
        et renvoie un tuple (table, colnames)'''

    conn_string = "host='localhost' dbname='" + config.dbname + "'" + \
                  "user='" + config.user + "' password=''" + \
                  " client_encoding='utf-8' "

    # print the connection string we will use to connect
    conn = psycopg2.connect(conn_string)
    del conn_string
    cur = conn.cursor()
    print("Connected!")
    command = "SELECT * FROM " + schema + "." + table_name
    cur.execute(command)
    colnames = [desc[0] for desc in cur.description]
    return (cur.fetchall(), colnames)


# -- Create table
def create_table(df, table_name, schema):
    conn_string = r'postgresql://' + config.user + ':''@localhost' + \
        '/' + config.dbname
    engine = create_engine(conn_string, client_encoding='utf-8')

    del conn_string

    return df.to_sql(table_name, engine, schema=schema, if_exists='replace')

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
