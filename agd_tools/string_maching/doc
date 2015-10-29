Ce dossier veut rassembler des outils pour aider à résourdre un problème
classique : le matching de chaine de caractères.

En effet, que ce soit pour des noms propres, pour des adresses ou encore, par
 exemple, pour des noms de médicaments ou des noms de départements,
 les informations codées sous forme de caractères sont parfois des informations
 centrales qui peuvent permettre de fusionner des jeux de données.

Le schéma général est le suivant :
- déterminer une forme standard
- utiliser un score de distance
- regrouper les éléménets les plus proches, identifier les non-matchs

## Définir une forme standard

L'idée de la définition d'un standard est de tout écrire sous une même forme.
Cette étape n'est pas obligatoire puisque la suite du programme pourra, par
exemple, réussi à matcher "Fécamp" avec "fecamp" ou "FECAMP". On peut voir cette
étape comme une étape de pre-processing dans laquelle on introduit tout ce que
l'on sait sur les différences possibles sur les chaines de caractères et comment
elles ont été codées.
On facilite en effet la deuxième étape lorsque l'on dit que "douze bis avenue
Jean Jaurès" est la même chose que "12b av. J. Jaurès"

La forme standard est spécifique à chaque problème. On voudra parfois que
"Monsieur Coppe" et "Monsieur Coppé" soit différent, parfois non.


### Exemples de formes standard :
 - lettres sans accent, sans majuscule et sans abréviation
 - caractères en utf-8 où "avenue" est remplacée par "av."
 - remplacement des noms de pays en anglais par une traduction en français
 - éléments phonétiques
 - ...


## Définir une distance

Lorsque les deux chaines sont identiques, on peut dire que la
distance est nulle et effectuer le matching.

Il y a ensuite des distances pré-existentes chacune avec leur spécificté. On peut
les utiliser comme telles ou bien les "hacker" un peu.
- [Distance de Levenshtein](https://fr.wikipedia.org/wiki/Distance_de_Levenshtein)
- [Distance de Damerau-Levenshtein](https://fr.wikipedia.org/wiki/Distance_de_Damerau-Levenshtein)
- [Distance de Jaro-Winkler](https://fr.wikipedia.org/wiki/Distance_de_Jaro-Winkler)
- [Distance de Hamming](https://fr.wikipedia.org/wiki/Distance_de_Hamming)
- ...


## Réaliser le matching

Lorsque l'on veut faire un matching strict on rapproche les chaînes de
  caractères identiques.
Ensuite, il y a des chaines plus ou moins proches, il faut alors définir ce que
l'on considère acceptable ou non.
