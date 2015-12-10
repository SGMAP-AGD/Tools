# Guide pratique de l'anonymisation

L'anonymisation est un processus mis en oeuvre lors de certains traitements de données personnelles. Il vise, dans un jeu de donné publié, à empêcher un utilisateur d'effectuer les actions suivantes:

* Distinguer un individu.
* Relier des informations relatives à un individu.
* Inférer de nouvelles informations concernant un individu.

L'anonymisation ne se limite pas à la suppression des champs identifiants d'un jeu de données, comme le nom ou l'adresse d'une personne. D'autres variables, qualifiées de réidentifiantes, peuvent être utilisées pour reconnaître un individu au sein d'un jeu de données. Il est donc nécéssaire de mettre en oeuvre des techniques plus avancées d'anonymisation, comme la généralisation dont nous allons décrire ici le processus.

## Classement des variables

Une des première étapes du processus d'anonymisation consiste à classer les variables en 3 catégories:

* Variables identifiantes: Il s'agit des variables qui, une fois isolées, permettent toujours la réidentification d'un individu. Un prénom et un nom de famille, une adresse mail ou un numéro de téléphone sont des variables réidentifiantes.
* Variables quasi-identifiantes: Les variables quasi-identifiantes ne permettent la réidentification d'un individu que lorsqu'elles sont reliées à d'autres variables. L'âge ou le sexe d'un individu ne sont pas des variables identifiantes, mais peuvent le devenir lorsque le lieu de résidence de l'individu est dévoilé.
* Variables sensibles: 

## Variables identifiantes

Les variables identifiantes sont obfusquées ou tout simplement retirées lors de l'anonymisation. On parle alors de pseudonymisation une fois cette étape passée. Le jeu de données n'est à ce stade pas encore anonymisé. 

### Obfuscation

Parfois, certaines variables identifiantes ne doivent pas être retirées du jeu de données anonymisé. C'est par exemple le cas lorsque le jeu données servira à analyser des parcours utilisateur. Chaque ligne représente alors un évenement. Un identifiant individuel apparait alors plusieurs fois dans le jeu de données anonymisé. Il convient ici d'obfusquer cet identifiant pour ne pas le dévoiler et ainsi restreindre son caractère identifiant au jeu de données en question.

La méthode retenue dans ce cas est celle du [hachage](https://fr.wikipedia.org/wiki/Fonction_de_hachage) des champs concernés. Les champs concernés doivent être hachés en utilisant un algorithme issu de la famille [SHA-2 ou SHA-3](http://csrc.nist.gov/publications/fips/fips180-4/fips-180-4.pdf), les plus robustes à l'heure actuelle. Ces fonctions étant largement utlisées dans le monde de l'informatique, elles sont disponibles dans les blibliothèques cryptographiques de chaque langage de programmation. Par exemple:

R: [digest](https://cran.rstudio.com/web/packages/digest/index.html)
Python: [hashlib](https://docs.python.org/3.5/library/hashlib.html)
SAS: [Call Routines](https://support.sas.com/documentation/cdl/en/lefunctionsref/67960/HTML/default/viewer.htm#p04sqiymw1a6unn1uvh943eudcvz.htm)
Java: [MessageDigest](http://docs.oracle.com/javase/8/docs/api/java/security/MessageDigest.html)

## Varables quasi-identifiantes et K-anonymat

## Variables sensibles et L-Diversité

* Les cas des variables manquantes


## Risques

* Hacking L diversity
* Inférence entre variables
* Jeux de données mutiples
* 


## Bibliographie
[ARTICLE 29 DATA PROTECTION WORKING PARTY](http://ec.europa.eu/justice/data-protection/article-29/documentation/opinion-recommendation/files/2014/wp216_en.pdf)