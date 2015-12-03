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

import pandas as pd


class Node():
    ### Functions used for tree construction

    def __init__(self, transformer):
        self.transformer = transformer  # initialisation du tansformer en param
        self.children = []  # chaque Node() possède des enfants (hors feuilles)
        self.transformer_output = None  # change lors de l'execution

    def add_child(self, transformer):
        """ Ajoute un enfant """
        # -- l'enfant est initialisé pour execution
        child = Node(transformer)
        # -- puis ajouté à la liste des enfants
        self.children.append(child)
        return child

    def get_child(self, transformer):
        # -- Le transformer est-il présent parmi les enfants du self.Node ?
        for c in self.children:
            if c.transformer == transformer:
                return c
        return self.add_child(transformer)

    def add_leaf(self, genealogy):
        # -- Construction de la généalogie
        older_ancestror, *younger_ancestrors = genealogy
        # -- On get_child le plus vieux (FeatureChoice: 1er de liste)
        child = self.get_child(older_ancestror)
        # -- Ensuite, on recommence pour tous les enfants jusqu'au + jeune
        if younger_ancestrors:
            child.add_leaf(younger_ancestrors)

    ### Functions used to process the tree in a depth first search way

    def depth_first_search_execute(self, transformer_input):
        """ Execution de l'arbre
        go as deep as possible, then backtracking and try to go as deep
        as possible, then backtracking.... until its finish
        https://www.youtube.com/watch?v=zLZhSSXAwxI
        """
        # -- Output = l'execution du transformer_input
        self.transformer_output = self.transformer.execute(transformer_input)
        if self.children == []:  # Lorsqu'on arrive à la feuille
            print(self.transformer_output)
            return  # Le résultat est stocké dans la feuille

        # -- Récursif : on relance la fonction pour les enfants
        #                  jusqu'à ce qu'il n'y en ai plus.

        for c in self.children:
            c.depth_first_search_execute(self.transformer_output)

        self.transformer_output = None  # free memory !

    def depth_first_search_print(self, result_list, genealogy):
        """Print des résultats de l'arbre"""
        genealogy.append(repr(self.transformer))
        # -- On ne print que les transformer_output des feuilles.
        if self.children == []:
            final_genealogy = genealogy.copy()
            result_list.append((final_genealogy, self.transformer_output))

        for c in self.children:
            c.depth_first_search_print(result_list, genealogy)
        genealogy.pop()


### -- Function to output results
class OutputResults():

    def __init__(self, result_list):
        self.result_list = result_list

    def compute_result_table(self, result_list):
        """
        paramètres : result_list, issue de l'execution de
                     depth_first_search_print()
        returns : un dataframe où chaque ligne est une genalogy de la forme
                  (import, feature_choice, feature_selection, AUC)
        but : rendre plus lisibe l'output brut de dfs_print()
        """
        result_list = self.result_list
        result_table = pd.DataFrame(columns=["import", "features_choice",
                                             "features_selection",
                                             "classifiers", "AUC"])
        for genealogy in range(0, len(result_list)):
            tmp = pd.DataFrame(result_list[genealogy][0]).T
            tmp.columns = ["import", "features_choice",
                           "features_selection", "classifiers"]
            tmp['AUC'] = result_list[genealogy][1]
            result_table = pd.concat([result_table, tmp], axis=0)
        tmp = None  # free memory
        return result_table

    def output_best_clf(self, result_list):
        """
        paramètres : result_list, issue de l'execution de
                     depth_first_search_print()
        returns : la genealogy ainsi que les paramètres associées ayant obtenu
                  le meilleur AUC.
        """
        result_list = self.result_list
        result_table = self.compute_result_table(result_list)
        best_clf = result_table[result_table.AUC ==
                                max(result_table.AUC)].classifiers
        return best_clf.tolist()
