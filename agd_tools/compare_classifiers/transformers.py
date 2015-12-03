# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:49:58 2015

@author: Michel, Flo
"""
import numpy as np
import pandas as pd

from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix, f1_score, log_loss
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

from STSISI.python import clean_table


# -- REGLES
#  Les trans

# -- Transformeurs
class Transformer():
    """
    What : Classe des transformeurs (interface = documentation sur la classe)
    Règle : les transformeur prennent en entrée un "transformeur_input"
            et sortent un "transformeur_output" (parfois triplet).
    > Toutes les classes de transformer auront cette structure !
    """
    def __init__(self):
        """initialisation"""
        pass

    def execute(transformer_input):
        """ execution et return d'un nouveau transformer"""
        pass

    def __str__(self):
        """ convert transformers into string, for readable output """
        return "This is a transformer"

    def __repr__(self):
        """ représentation sur-mesure d'un transformer et de ses paramètres """
        return "%s (%s)" % (self.__class__.__name__, self.__dict__)


#  -- Import
class ImportTransformer(Transformer):
    """ Import de toutes les données """
    def __init__(self):
        self.iris = True
        self.patrouilles = True
        self.history = True
        self.calendar = True
        self.meteo = True
        self.iris_dummy = True

    def execute(self, transformer_input):  # On importe tout
        transformer_output = clean_table.construct_XY(iris=self.iris,
                                                      patrouilles=self.patrouilles,
                                                      history=self.history,
                                                      calendar=self.calendar,
                                                      meteo=self.meteo,
                                                      iris_dummy=self.iris_dummy)
        return transformer_output  # Triplet


#  -- Choice
class FeatureChoice(Transformer):
    """ Choix des données"""
    def __init__(self, features_choice):  # ex = ["iris", "meteo"]
        self.features_choice = features_choice

    def execute(self, transformer_input):
        """
        parametres : un triplet (XY_train, XY_test, dict_features)
        return : Y_train, Y_test +  X_train et X_test contenant les features
                 selectionnées par l'utilisateur (quadruplet)
        """
        (XY_train, XY_test, dict_features) = transformer_input
        features_output = []

        for f in self.features_choice:
            features_output += dict_features[f]
            #  Renvoie la liste des variables ("WW_mean", ...)
            #  par features ("meteo")
        print("Il y a %s features selectionnées dans FeatureChoice"
              % (len(features_output)))
        transformer_output = (XY_train.loc[:, 'Y'],
                              XY_test.loc[:, 'Y'],
                              XY_train.loc[:, features_output],
                              XY_test.loc[:, features_output])
        return transformer_output


# -- Feature Selection
class FeatureSelection(Transformer):
    """
    Classe des selections de features (Transformer)
    """
    def __init__(self):
        pass


class FeatureSelectionRF(FeatureSelection):

    def __init__(self, param_choice_dict):
        # Initialiser tous les paramètres de la RF
        self.n_estimators = param_choice_dict['n_estimators']
        self.max_depth = param_choice_dict['max_depth']
        self.bootstrap = param_choice_dict['bootstrap']
        self.criterion = param_choice_dict['criterion']
        self.class_weight = param_choice_dict['class_weight']
        self.n_jobs = param_choice_dict['n_jobs']

        # Seuil de selection
        self.threshold = param_choice_dict['threshold']

    def execute(self, transformer_input):
        """
        parametres : un quadruplet (Y_train, Y_test, X_train, X_test) contenant
                     les features selectionnées
        return : X_train_rf et X_test_rf contenant les features selectionnées
                 par Random Forest
        """
        (Y_train, Y_test, X_train, X_test) = transformer_input
        model_rf = RandomForestClassifier(n_estimators=self.n_estimators,
                                          max_depth=self.max_depth,
                                          bootstrap=self.bootstrap,
                                          criterion=self.criterion,
                                          class_weight=self.class_weight,
                                          n_jobs=self.n_jobs)

        fitted_model_rf = model_rf.fit(X_train, Y_train)

        X_train_rf = SelectFromModel(fitted_model_rf,
                                     threshold=self.threshold,
                                     prefit=True).transform(X_train)

        X_test_rf = SelectFromModel(fitted_model_rf,
                                    threshold=self.threshold,
                                    prefit=True).transform(X_test)

        n_features = X_train.shape[1]
        n_features_selected = X_train_rf.shape[1]
        print("Il y a %s - %s = %s features restantes suite à la RF"
              % (n_features, (n_features-n_features_selected),
                 n_features_selected))

        transformer_output = (Y_train, Y_test, X_train_rf, X_test_rf)
        return transformer_output


class FeatureSelectionLR(FeatureSelection):

    def __init__(self, param_choice_dict):
        # Initialiser tous les paramètres de la RF
        self.Cs = param_choice_dict['Cs']
        self.fit_intercept = param_choice_dict['fit_intercept']
        self.dual = param_choice_dict['dual']
        self.penalty = param_choice_dict['penalty']
        self.scoring = param_choice_dict['scoring']
        self.solver = param_choice_dict['solver']
        self.tol = param_choice_dict['tol']
        self.max_iter = param_choice_dict['max_iter']
        self.class_weight = param_choice_dict['class_weight']
        self.n_jobs = param_choice_dict['n_jobs']
        self.refit = param_choice_dict['refit']

    def execute(self, transformer_input):
        """
        parametres : un quadruplet (Y_train, Y_test, X_train, X_test) contenant
                     les features selectionnées
        return : X_train_ridge et X_test_ridge contenant les features
                 selectionnées par Ridge
        """
        (Y_train, Y_test, X_train, X_test) = transformer_input
        lcv = LogisticRegressionCV(Cs=self.Cs,
                                   fit_intercept=self.fit_intercept,
                                   dual=self.dual,
                                   penalty=self.penalty,
                                   scoring=self.scoring,  # essayer avec f1 ?
                                   solver=self.solver,
                                   tol=self.tol,
                                   max_iter=self.max_iter,
                                   class_weight=self.class_weight,
                                   n_jobs=self.n_jobs,
                                   refit=self.refit)

        model_lcv = lcv.fit(X_train, Y_train)

        X_train_ridge = SelectFromModel(model_lcv, prefit=True).transform(X_train)
        X_test_ridge = SelectFromModel(model_lcv, prefit=True).transform(X_test)

        n_features = X_train.shape[1]
        n_features_selected = X_train_ridge.shape[1]
        print("Il y a %s - %s = %s features restantes suite à la Ridge"
              % (n_features, (n_features-n_features_selected),
                 n_features_selected))

        transformer_output = (Y_train, Y_test, X_train_ridge, X_test_ridge)
        return transformer_output


#  -- Classifieurs
class Classifier(Transformer):
    """
    La classe des classifieurs
    """
    def __init__(self):
        pass


class ClassifierRF(Classifier):

    def __init__(self, param_choice_dict):
        # Initialiser tous les paramètres de la RF
        self.n_estimators = param_choice_dict['n_estimators']
        self.class_weight = param_choice_dict['class_weight']
        self.criterion = param_choice_dict['criterion']
        self.bootstrap = param_choice_dict['bootstrap']
        self.max_features = param_choice_dict['max_features']
        self.min_samples_split = param_choice_dict['min_samples_split']
        self.min_samples_leaf = param_choice_dict['min_samples_leaf']
        self.max_depth = param_choice_dict['max_depth']
        self.n_jobs = param_choice_dict['n_jobs']
        # Initialiser tous les paramètres du Adaboost(RF)
        self.n_estimators_ADA = param_choice_dict['n_estimators_ADA']
        self.random_state_ADA = param_choice_dict['random_state_ADA']
        self.learning_rate_ADA = param_choice_dict['learning_rate_ADA']
        self.boosted_RF = param_choice_dict['boosted_RF']  # boolean

    def execute(self, transformer_input):
        """
        parametres : un quadruplet (Y_train, Y_test, X_train_sfm, X_test_sfm)
                     contenant les features selectionnées par RF
        return : un triplet (output_RF, predict_probas_RF, roc_auc_RF)
                 contenant les résultats du clf Random Forest.
        """
        #  sfm = Select From Model
        (Y_train, Y_test, X_train_sfm, X_test_sfm) = transformer_input
        # -- Classifier RF
        np.random.seed(100)  # Il faudra penser à intégrer les SEED
        clf_RF = RandomForestClassifier(n_estimators=self.n_estimators,
                                        class_weight=self.class_weight,
                                        criterion=self.criterion,
                                        bootstrap=self.bootstrap,
                                        max_features=self.max_features,
                                        min_samples_split=self.min_samples_split,
                                        min_samples_leaf=self.min_samples_leaf,
                                        max_depth=self.max_depth,
                                        n_jobs=self.n_jobs)

        fitted_clf_RF = clf_RF.fit(X_train_sfm, Y_train)

        # -- compute results of RF
        predict_proba_RF = fitted_clf_RF.predict_proba(X_test_sfm)[:, 1]
        #output_RF = fitted_clf_RF.predict(X_test_sfm)
        auc_RF = roc_auc_score(Y_test, predict_proba_RF)

        if self.boosted_RF:
            # -- Classifier Adaboost(RF)
            clf_ADA = AdaBoostClassifier(clf_RF,
                                         n_estimators=self.n_estimators_ADA,
                                         random_state=self.random_state_ADA,
                                         learning_rate=self.learning_rate_ADA)

            fitted_clf_ADA = clf_ADA.fit(X_train_sfm, Y_train)

            # -- compute results of Adaboost(RF)
            predict_probas_ADA = fitted_clf_ADA.predict_proba(X_test_sfm)[:, 1]
            #output_ADA = fitted_clf_ADA.predict(X_test_sfm)
            auc_ADA = roc_auc_score(Y_test, predict_probas_ADA)

            transformer_output = [auc_RF, auc_ADA]

        else:
            transformer_output = auc_RF

        return transformer_output


class ClassifierLR(Classifier):

    def __init__(self, param_choice_dict):
        self.class_weight = param_choice_dict['class_weight']
        self.max_iter = param_choice_dict['max_iter']
        self.n_jobs = param_choice_dict['n_jobs']

    def execute(self, transformer_input):
        """
        parametres : un quadruplet (Y_train, Y_test, X_train_sfm, X_test_sfm)
                     contenant les features selectionnées par RF
        return : un triplet (output_RF, predict_probas_RF, roc_auc_RF)
                 contenant les résultats du clf Random Forest.
        """
        (Y_train, Y_test, X_train_sfm, X_test_sfm) = transformer_input

        # -- Classifier RF
        clf_LR = LogisticRegression(class_weight=self.class_weight,
                                    max_iter=self.max_iter,
                                    n_jobs=self.n_jobs)

        fitted_clf_LR = clf_LR.fit(X_train_sfm, Y_train)
        # -- compute results of LR
        predict_probas_LR = fitted_clf_LR.predict_proba(X_test_sfm)[:, 1]
        #output_LR = clf_LR.predict(X_train_sfm)
        auc_LR = roc_auc_score(Y_test, predict_probas_LR)

        transformer_output = auc_LR
        return transformer_output


class ClassifierLRConstant(Classifier):

    def __init__(self, param_choice_dict):
        self.class_weight = param_choice_dict['class_weight']
        self.max_iter = param_choice_dict['max_iter']

    def execute(self, transformer_input):
        """
        parametres : un quadruplet (Y_train, Y_test, X_train_sfm, X_test_sfm)
                     contenant les features selectionnées par RF
        return : un triplet (output_RF, predict_probas_RF, roc_auc_RF)
                 contenant les résultats du clf Random Forest.
        """
        (Y_train, Y_test, X_train_sfm, X_test_sfm) = transformer_input

        # -- Classifier LRConstant
        clf_LRConstant = LogisticRegression(class_weight=self.class_weight,
                                            max_iter=self.max_iter)
        fitted_clf_LRConstant = clf_LRConstant.fit(X_train_sfm, Y_train)
        # -- compute results of LR on X_train (not test !)
        overfitted_probas_LRConstant = pd.Series(fitted_clf_LRConstant.predict_proba(X_train_sfm)[:, 1])

        # -- Solution dégueulasse et temporaires pour avoir les individus
        (XY_train, XY_test, dict_features) = clean_table.construct_XY(history=True)  # import le plus simple possible
        ref_iris_train = XY_train.reset_index()[['date', 'DCOMIRIS']].copy()
        ref_iris_test = XY_test.reset_index()[['date', 'DCOMIRIS']].copy()

        # -- Concat des probabilités obtenues avec les individus du train
        t_prob_train = pd.concat([overfitted_probas_LRConstant,
                                  ref_iris_train], axis=1)
        t_prob_train.columns = ['overfitted_probas_LRConstant', 'date',
                                'DCOMIRIS']
        # -- Calcul des probabilités moyennes par individu (DCOMIRIS)
        t_prob_moy = t_prob_train.groupby('DCOMIRIS')['overfitted_probas_LRConstant'].mean()

        # -- Répartition des probas de chaque indivdu sur le test
        t_prob_moy_test = pd.DataFrame()
        t_prob_moy_test = pd.merge(t_prob_moy.reset_index(),
                                   ref_iris_test, on='DCOMIRIS')

        # -- Calcul de la roc_auc sur le test
        t_prob_test = t_prob_moy_test['overfitted_probas_LRConstant'].as_matrix()
        auc_LRConstant = roc_auc_score(Y_test, t_prob_test)

        transformer_output = auc_LRConstant
        return transformer_output
