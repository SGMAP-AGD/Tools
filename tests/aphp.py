import pandas as pd
import numpy as np

from agd_tools import anonymization

anon_motif = pd.read_csv("/home/paul/Documents/APHP/anon_motif.csv",sep=";")

for name, group in anon_motif.groupby(['SITE','ANNEE_ENTREE','MOIS_ENTREE','JOUR_ENTREE']):
    uniques = group['MOTIFMED1'].unique()
    # print(len(uniques))
    if(len(group)<5):
        print("alert")
    if(len(uniques)<3):
        if(uniques.all() != np.array(['0'])):
            print(group.groupby(['MOTIFMED1']).agg(['count'])['SITE'])
   

#iris = pd.read_csv("https://raw.github.com/pydata"
             #              "/pandas/master/pandas/tests/data/iris.csv")
#iris_anonymized = iris[['Name']]
#print(anonymization.get_k(iris_anonymized))
