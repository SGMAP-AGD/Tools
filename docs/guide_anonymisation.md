# Guide pratique de l'anonymisation

L'anonymisation est un processus mis en oeuvre lors de la publication de données personelles. Il vise, dans un jeu de donné publié, à:

* Empêcher de distinguer un individu.
* Interdire la liaison d'informations relatives à un individu.
* Empêcher l'inférence d'informations concernant un individu. 

## Classement des variables

Une des première étapes du processus d'anonymisation consiste à classer les variables en 3 catégories:

* Variables identifiantes
* Variables quasi-identifiantes: 
* Variables sensibles

## Variables identifiantes

Les variables identifiantes sont obfusquées ou tout simplement retirées lors de l'anonymisation.
On parle alors de pseudonymisation une fois cette étape passée. Le jeu de données n'est à ce stade pas encore anonymis.

### Obfuscation

Parfois, certaines variables identifiantes ne doivent pas être retirées du jeu de données anonymisé.
C'est par exemple le cas lorsque le jeu données servira à analyser des parcours utilisateur et qu'un
identifiant individuel apparaitra plusieurs fois dans le jeu de données anonymisé.
Il convient alors d'obfusquer cet identifiant pour ne pas le dévoiler tout en préservant son caractère particulier.

La méthode retenue dans ce cas est celle du hachage des champs concernés.


## Anonymisation par généralisation

Lors d'une anonymisation par aggrégation, les variables 

## K-anonymat

## L-Diversité

## Mesurer la perte d'informations

ARTICLE 29 DATA PROTECTION WORKING PARTY
http://ec.europa.eu/justice/data-protection/article-29/documentation/opinion-recommendation/files/2014/wp216_en.pdf