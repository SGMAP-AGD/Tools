# -*- coding: utf-8 -*-
"""
Run a tree of experiments, loading and transforming only once for each step.

Created on Wed Nov 25 17:20:05 2015.

@author: Michel ,Flo
"""

import pandas as pd
from agd_tools.compare_classifiers import transformers
from sklearn.metrics import roc_auc_score, roc_curve, auc
from matplotlib import pyplot as plt

import clean_table

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

    def depth_first_search_results(self, result_list, genealogy):
        """Collecte les résultats de l'arbre."""
        genealogy.append(repr(self.transformer))
        # -- On ne print que les transformer_output des feuilles.
        if self.children == []:
            final_genealogy = genealogy.copy()
            result_list.append((final_genealogy, self.transformer_output))

        for c in self.children:
            c.depth_first_search_results(result_list, genealogy)
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
        root_tr = transformers.TransformerId()    # init ImportTransformer
        self.root = Node(root_tr)  # construct the root
        self.add_tasks(tasks_list)   # construct the rest of the tree

        self.result_list = []
        self.genealogy = []

        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None
        self.dict_features = None

    def run(self):
        nuplet = clean_table.construct_XY(
            iris=False,
            patrouilles=False,
            history=True,
            calendar=False,
            meteo=False,
            iris_dummy=False)
        self.X_train, self.X_test, self.Y_train, self.Y_test, self.dict_features = nuplet

        self.root.depth_first_search_execute(
            (self.X_train, self.X_test, self.Y_train, self.dict_features))

    def get_results(self):
        self.result_list = []
        self.genealogy = []
        self.root.depth_first_search_results(self.result_list, self.genealogy)

    def get_table(self):
        """
        Give pretty table summarizing the tasks and their ROC AUC.
        """
        results = list(map(lambda r: r[0] + [r[1]], self.result_list))
        table = pd.DataFrame(results)
        table.columns = ["Import", "Feature Choice", "Feature Selection", "Classifier", "proba"]
        table['AUC'] = table.proba.map(lambda p: roc_auc_score(self.Y_test, p))
        table.drop(['Import'], axis=1, inplace=True)
        table.drop(['proba'], axis=1, inplace=True)
        return(table)

    def get_roc(self, indexes):
        """
        Compute ROC curves for tasks whose indexes are listed in 'indexes'.

        The curves are plotted with pyplot. They are labeled by their indexes
        in the 'results' list of the Tree. Use 'get_table' to get details about
        the corresponding tasks.
        """
        results = list(map(lambda r: r[0] + [r[1]], self.result_list))
        table = pd.DataFrame(results)
        table.columns = ["Import", "Feature Choice", "Feature Selection", "Classifier", "proba"]
        roc_curves = table.proba.map(lambda p: roc_curve(self.Y_test, p))

        plt.figure()
        for i in indexes:
            roc = roc_curves[i]
            plt.plot(roc[0], roc[1], label='ROC curve n°%d (area = %0.2f)' % (i, auc(roc[0], roc[1])))
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristics')
        plt.legend(loc="lower right")
        plt.show()
