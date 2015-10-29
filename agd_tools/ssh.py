#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser

import paramiko
import pandas as pd

__author__ = "Florian, Paul"

""" Read config file """
config = configparser.ConfigParser()
config.read("config.ini")


def get_connect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config["SSH"]["host"],
                username=config["SSH"]["username"])
    return ssh


def export_df(df, remotepath, sep=";"):

    """ Save df to local csv """
    current_dir = os.getcwd()
    filepath = current_dir + "/temp.csv"
    df.to_csv(path_or_buf=filepath,
              sep=sep)

    """ Put the csv over sftp """
    ssh = get_connect()
    sftp = ssh.open_sftp()
    sftp.put(filepath, remotepath)

    """ Delete local csv """
    os.remove(filepath)

    """ Close ssh """
    ssh.close()


def import_csv(path, filename):
    """ crée une connexion sftp sur le server secure et permet notamment
    l'accès à des fichiers contenus sur le server"""
    ssh = get_connect()
    sftp = ssh.open_sftp()
    sftp.chdir(path)
    df = pd.read_csv(sftp.open(filename))
    ssh.close()
    return df


def remove_file(remotepath):
    ssh = get_connect()
    sftp = ssh.open_sftp()
    sftp.remove(remotepath)
