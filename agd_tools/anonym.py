# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 19:28:44 2015

@author: Alexis
"""

import pandas as pd


class AnonymDataFrame(object): 
    
    def __init__(self, df, var_identifiantes, var_sensibles):
        assert isinstance(df, pd.DataFrame)                
        self.df = df
        
        columns = df.columns
        for var in [var_identifiantes, var_sensibles]:
            assert isinstance(var, list)
        assert all([x in columns for x in var_identifiantes])
        assert all([x in columns for x in var_sensibles])
        assert len(set(var_identifiantes) | set(var_sensibles))
        self.identifiant = var_identifiantes
        self.sensible = var_sensibles
        
    def list_valeurs_identifiantes(self):
        for var in self.identifiant:
            print(self.df[var].unique())
        
        
    def get_k(self):
        taille_des_groupes = self.df.groupby(self.identifiant).size()
        return min(taille_des_groupes)

tab['annee_naiss'] = tab['date_naiss'].str[6:]
test = AnonymDataFrame(tab, ['annee_naiss', 'sexe', 'robe'], ['nom', 'conso'])
test.list_valeurs_identifiantes()


        