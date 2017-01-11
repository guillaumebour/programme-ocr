# Reconnaissance de codes postaux par ordinateur

Ce projet est un programme de reconnaissance optique de caractères (OCR) développé dans le cadre du TIPE du deuxième année de CPGE.
Il permet la reconnaissance d'un code postal à partir d'un scan manuscrit.

L'objectif était de découvrir le fonctionnement d'un OCR et d'en développer un en partant de zéro.

Ainsi les fonctions de bases telles que le seuillage, le calcul d'un histogramme ou la détection des contours ont été réimplémentées.

L'algorithme de reconnaissance utilisé est simple, il s'agit de l'algorithme des k plus proches voisins (https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm).

Les résultats obtenus varient selon l'image utilisée, les échantillons utilisés comme références n'étant pas nombreux (60 / chiffre).


## Modes de fonctionnement

Le programme peut fonctionner avec quelques variations :
- l'utilisation ou non d'une base de données en cas de doute pour donner la liste des codes postaux possibles

  Ex: dans Principale.py utiliser les paramètres suivant sur l'image fournie :
  - affichage_intermediaire = True
  - utilisation_bdd = True
  - utilisation_scores = True

- le choix par le programme du code qu'il pense être le bon, et la recherche des informations concernant ce code dans la BDD

  Ex: dans Principale.py utiliser les paramètres suivant sur l'image fournie :
  - affichage_intermediaire = True
  - utilisation_bdd = False
  - utilisation_scores = True


## Structure du projet :
  - data : contient les données du projet (scans, .csv).
    - database : contient les données nécessaires à la création de la DB, et le fichier sqlite crée lors de l'exécution.
    - scanSet : contient le jeu de test et les scans (possibilité d'en ajouter, il suffit de respecter le format et la convention de nommage).
  - images : contient les images à traiter.
  - results : contient des données supplémentaires, notamment sur la validation croisée dont l'exécution est très lente.
  - scripts : scripts shell du projet
  - src : les sources du projet, contenant les 6 fichiers Python. Principale.py étant le fichier à exécuter. La première exécution est plus lente car elle crée la base de données ainsi que le jeu de test.
  

## Détails des versions 
  
### v1.0.0 Version initiale
  
Version fonctionnelle du projet comprenant les fonctionnalités:
- de traitement de l'image (réimplémentées)
- de détection de contours
- de reconnaissance avec l'algorithme des k-plus-proches-voisins
- de génération du jeu de données
- de recherche et d'amélioration des résultats dans la base de données.
  
  
