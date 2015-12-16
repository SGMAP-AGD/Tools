# -*- coding: utf-8 -*-
"""
Run a tree of experiments, loading and transforming only once for each step.

Created on Wed Nov 25 17:20:05 2015.

@author: Michel ,Flo
"""

import pandas as pd
from agd_tools.compare_classifiers import transformers


class Node():
    """Implementation of the nodes of the tree.

    This class should not be used outside.
    """

    def __init__(self, transformer):
        """Construct the tree."""
        self.transformer = transformer  # initialisation du tansformer en param
        self.children = []  # chaque Node() possède des enfants (hors feuilles)
        self.transformer_output = None  # change lors de l'execution

    def add_child(self, transformer):
        """Ajoute un enfant."""
        # -- l'enfant est initialisé pour execution
        child = Node(transformer)
        # -- puis ajouté à la liste des enfants
        self.children.append(child)
        return child

    def get_child(self, transformer):
        """Get a child.

        Get a child having the same transformer as given in parameter.
        If such a child does not exist, create it.
        """
        # -- Le transformer est-il présent parmi les enfants du self.Node ?
        for c in self.children:
            if c.transformer == transformer:
                return c
        return self.add_child(transformer)

    def add_leaf(self, genealogy):
        """Add a leaf given whole genealogy from current node."""
        # -- Construction de la généalogie
        older_ancestror, *younger_ancestrors = genealogy
        # -- On get_child le plus vieux (FeatureChoice: 1er de liste)
        child = self.get_child(older_ancestror)
        # -- Ensuite, on recommence pour tous les enfants jusqu'au + jeune
        if younger_ancestrors:
            child.add_leaf(younger_ancestrors)

    # Functions used to process the tree in a depth first search way

    def depth_first_search_execute(self, transformer_input):
        """Execution de l'arbre.

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
        """Print des résultats de l'arbre."""
        genealogy.append(repr(self.transformer))
        # -- On ne print que les transformer_output des feuilles.
        if self.children == []:
            final_genealogy = genealogy.copy()
            result_list.append((final_genealogy, self.transformer_output))

        for c in self.children:
            c.depth_first_search_print(result_list, genealogy)
        genealogy.pop()


class Tree():
    """ Tree of experiments.
    """

    def add_tasks(self, tasks_list):
        """Fonction permettant de construire l'arbre."""
        for task in tasks_list:
            self.root.add_leaf(task)

    def __init__(self, tasks_list):
        """Construct the tree."""
        self.result_list = []
        self.genealogy = []

        import_0 = transformers.ImportTransformer()    # init ImportTransformer
        self.root = Node(import_0)  # construct the root
        self.add_tasks(tasks_list)   # construct the rest of the tree

    def run(self):
        self.root.depth_first_search_execute(None)

    def get_results(self):
        self.result_list = []
        self.genealogy = []
        self.root.depth_first_search_print(self.result_list, self.genealogy)

    def print_table(self):
        """
        Give pretty table output.

        returns : un dataframe où chaque ligne est une genalogy de la forme
                  (import, feature_choice, feature_selection, AUC)
        """
        pd.options.display.max_colwidth = 500
        result_table = pd.DataFrame(columns=["import", "features_choice",
                                             "features_selection",
                                             "classifiers", "AUC"])
        for genealogy in range(0, len(self.result_list)):
            tmp = pd.DataFrame(self.result_list[genealogy][0]).T
            tmp.columns = ["import", "features_choice",
                           "features_selection", "classifiers"]
            tmp['AUC'] = self.result_list[genealogy][1]
            result_table = pd.concat([result_table, tmp], axis=0)
        tmp = None  # free memory

        best_clf = result_table[result_table.AUC ==
                                max(result_table.AUC)].classifiers
        print(best_clf.tolist())
