# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:20:05 2015

@author: Michel ,Flo
"""


"""
deux objectifs :
1/ créer le graphe du parcours en profondeur
2/ ne pas répéter les transformations déjà en mémoire
"""


class Node():

    def __init__(self, transformer):
        self.transformer = transformer  # initialisation du tansformer en param
        self.children = []  # liste d'enfants
        self.transformer_output = None  # ?

    def add_child(self, transformer):
        """ Ajoute un enfant """
        child = Node(transformer)
        self.children.append(child)  # ajout d'un child à sa liste children
        return child

    def deep_first_search(self, transformer_input):
        """ récursif """
        transformer_output = self.transformer.execute(transformer_input)
        if self.children == []:  # Lorsqu'on arrive à la feuille
            print(transformer_output)
        for c in self.children:
            c.deep_first_search(transformer_output)
        transformer_output = None  # free memory !

    def get_child(self, transformer):
        for c in self.children:
            if c.transformer == transformer:
                return c

        return self.add_child(transformer)

    def add_leaf(self, genealogy):
        older_ancestror, *younger_ancestrors = genealogy
        child = self.get_child(older_ancestror)
        if younger_ancestrors:
            child.add_leaf(younger_ancestrors)
