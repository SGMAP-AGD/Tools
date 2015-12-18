#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import configparser

import paramiko
import pandas as pd

__author__ = "Florian, Paul, Alexis"

# Read config file
config = configparser.ConfigParser()
path_config = os.path.dirname(os.path.realpath(__file__))
config.read(os.path.join(path_config, "config.ini"))


def _get_connect():
    """ crée une connexion sftp sur le server secure et permet notamment
    l'accès à des fichiers contenus sur le server """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(config["SSH"]["host"],
                username=config["SSH"]["username"],
                key_filename=config["SSH"]["ssh_key"])

    return ssh


def export_df(df, remotepath, sep=";"):
    ''' exporter un pandas DataFrame en un csv sur le serveur
        - sep désigne le séparateur du csv
    '''
    # Save df to local csv
    current_dir = os.getcwd()
    filepath = os.path.join(current_dir, 'temp.csv')
    df.to_csv(path_or_buf=filepath, sep=sep)

    ssh = _get_connect()
    sftp = ssh.open_sftp()
    sftp.put(filepath, remotepath)  # Put the csv over sftp
    os.remove(filepath)  # Delete local csv
    ssh.close()


def import_csv(path, filename, sep=',', encoding='utf8'):
    """ import un csv depuis le serveur et renvoit un pandas DataFrame """
    ssh = _get_connect()
    sftp = ssh.open_sftp()
    sftp.chdir(path)
    df = pd.read_csv(sftp.open(filename), sep=sep, encoding=encoding)
    ssh.close()
    return df


def remove_file(remotepath):
    ''' supprime un fichier du serveur '''
    ssh = _get_connect()
    sftp = ssh.open_sftp()
    sftp.remove(remotepath)
    ssh.close()
