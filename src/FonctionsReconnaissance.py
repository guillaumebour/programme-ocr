#### Bibliotheque de fonctions pour la reconaissance de caractères ###
# @author: Guillaume Bour
# @date: 19-05-2016
# @description: Fichier regroupant des fonctions pour la reconnaissance de caractères
#
#
# Liste des fonctions implémentées:
#
# # Manipulation entrainement:
# - getImageAt
# - getImagesEntrainement
#
# # Calcul de distance:
# - verificationTailles
# - distanceNaive
# - distanceEuclidienne
# - distanceManhattan
#
# # Recherche distance:
# - rechercheDistanceMinToutesImages
# - rechercheDistanceMinMoyenneChiffres
#
# # K Plus Proches Voisins:
# - getKMin
# - kNN
#
# # Cross-Validation:
# - crossValidation_Holdout
#
# # Analyse:
# - getCaractereForPosition
#
#
## CONVENTIONS :
# -------------
#
# De base un texte a des caractères dont les traits sont en NOIR
# lorsqu'une fonction a un paramètre 'inv', les chiffres apparaissent donc en
# NOIR sur un fond BLANC si inv = False (par défaut)
# Si inv = True, ils apparaissent alors en BLANC sur fond NOIR
#
#
## COMMENTAIRES :
# --------------
#
#




# MODULES NECESSAIRES
import numpy as np 					# manipulation des images
import matplotlib.pyplot as plt 	# affichage des images
import time 						# calcul du temps d'execution


## Manipulation entrainement

def getImageAt(img, i, j, l=20, h=20):
	"""Pour une image qui contient un tableau d'autres images de dimension l*h, retourne l'image à la position (i,j).
	   L'image de coordonnées (0,0) est la première image en haut à gauche.
	   i est la colonne et j la ligne dans cette convention"""

	return img[j*h:(j+1)*h,i*h:(i+1)*h]


def getImagesEntrainement(img,proportion=60):
	"""Retourne les 2 parties du jeu d'entrainement selon les proportions.
		proportion : pourcentage pour le jeu d'entrainement sur l'image"""

	nbreCol = len(img[0])/20
	nbreColEntrainement = (nbreCol*proportion)//100

	return (img[:,:nbreColEntrainement*20],img[:,nbreColEntrainement*20:])



## Calcul de distance
def verificationTailles(m1, m2):
	"""Verfifie les tailles des matrices m1 et m2"""

	if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
		print("Erreur dans les dimensions des matrices !")
		print("M1 : {} {}".format(len(m1),len(m1[0])))
		print("M2 : {} {}".format(len(m2),len(m2[0])))

		return False

	return True


def distanceNaive(m1,m2):
	"""Fait la somme de m1 et m2 modulo 2, et retourne le nombre de 1, c'est à dire le nombre de points différents"""

	if not verificationTailles(m1, m2):
		return -1

	newMat = np.zeros((len(m1),len(m1[0])))
	d = 0

	for i in range(len(m1)):
		for j in range(len(m1[0])):
			newMat[i][j] = (m1[i][j]+m2[i][j])%2
			# On augmente le nombre de points différents
			if newMat[i][j] == 1:
				d+=1

	return d


def distanceManhattan(m1,m2):
	"""Calcul de la distance de 'Manhattan' pour m1 et m2"""

	if not verificationTailles(m1, m2):
		return -1

	d = 0

	for i in range(len(m1)):
		for j in range(len(m1[0])):
			d += abs(m1[i][j]-m2[i][j])

	return d


def distanceEuclidienne(m1,m2):
	"""Calcul la distance euclidienne pour m1 et m2"""

	if not verificationTailles(m1, m2):
		return -1

	d = 0

	for i in range(len(m1)):
		for j in range(len(m1[0])):
			d += (m1[i][j]-m2[i][j])**2

	return np.sqrt(d)



## Recherche de distance minimale

def rechercheDistanceMinToutesImages(img_entrainement, img_comparaison, distance, l=20, h=20):
	"""Boucle et calcul les distances entre les images de img_entrainement et img_comparaison pour la distance passée
	   en paramètre. Renvoie la distance minimale, et l'image associée (et donc sa position)"""

	dMin = l*h+1 # dans le "pire" des cas on a une image blanche et une image noire (pour distance naive)

	X = len(img_entrainement[0])
	Y = len(img_entrainement)

	img_actuelle = []
	position = (-1,-1)

	for i in range(X//l):
		for j in range(Y//h):
			img = getImageAt(img_entrainement,i,j,l,h) 	# récupération de l'image à la position (i,j)
			d = distance(img_comparaison,img)			# calcul de la distance
			if d < dMin:
				dMin = d
				img_actuelle = img
				position = (i,j)

	return dMin, position, img_actuelle


def rechercheDistanceMinMoyenneChiffres(img_entrainement, img_comparaison, distance, l=20, h=20):
	"""Fait la moyenne des distances pour chaque chiffre, et renvoie la plus petite"""

	X = len(img_entrainement[0])
	Y = len(img_entrainement)

	distancesMoy = [0,0,0,0,0,0,0,0,0,0] # (d0,d1,d2,...,d9)

	for i in range(Y//h):
		for j in range(X//l):
			img = getImageAt(img_entrainement,j,i,l,h)
			d = distance(img_comparaison, img)

			distancesMoy[i//5] += d

	dMin = distancesMoy[0]
	result = 0

	for i in range(len(distancesMoy)):
		if(distancesMoy[i]<dMin):
			dMin = distancesMoy[i]
			result = i

	return result, dMin/500



# IMPLEMENTATION K PLUS PROCHES VOISINS

def getKMin(tab,k):
	"""Retourne les k plus petites valeurs du tableau: [(distance1, i1,j1),(distance2, i2,j2)...]"""
	result = []

	# On recherche k fois le minimum, et on le passe à -1:
	for c in range(k):
		dMin = 400 # distance max
		position = (-1,-1)
		for i in range(len(tab)):
			for j in range(len(tab[0])):
				if tab[i][j] < dMin and tab[i][j] != -1:
					dMin = tab[i][j]
					position = (i,j)

		result.append((dMin,position[0],position[1]))
		tab[position[0]][position[1]] = -1

	return result


def kNN(img_comparaison, img_entrainement, k, distance = distanceEuclidienne, affichage = False, scores = True, db = True):
	"""Implémentation de la méthode des k plus proches voisins.
	   Entrée: L'image a reconnaitre (un seul caractère), l'image d'entrainement et k.
	   Sortie: La valeur reconnue sur l'image."""


	X = len(img_entrainement[0])
	Y = len(img_entrainement)

	matDistances = np.zeros((Y//20,X//20))

	# On commence par calculer la matrice des distances:
	for i in range(X//20):
		for j in range(Y//20):
			img = getImageAt(img_entrainement,i,j) 	# récupération de l'image à la position (j,i)
			d = distance(img_comparaison,img)		# calcul de la distance
			matDistances[j][i] = d 					# distance avec l'image à la position (j,i)

	# recherche des positions des k plus proches voisins (k plus petites distances)
	kppv = getKMin(matDistances,k)

	classes = [0,0,0,0,0,0,0,0,0,0]	# compteur des votes (0,1,2,3,4,5,6,7,8,9)

	# Pour chaque voisin, on regarde sa classe et on incrémente la case correspondante dans classes:
	for voisin in kppv:
		c = voisin[1]//5
		classes[c] += 1

	# on recherche le plus grand à l'issu du comptage:
	maxC = 0
	ind = 0

	for i in range(len(classes)):
		if classes[i] > maxC:
			maxC = classes[i]
			ind = i

	if affichage:
		print("Résultat du vote: {}".format(classes))

	if scores and db == False: # le score ne s'execute seul que si db est faux

		# on doit tester le 'score' de la determination : (score sur 10)
		score = int(classes[ind]/k*10)

		if affichage:
			print("- Score : {}".format(score))

		# si le score est inférieur à 5 strictement, on regarde le second meilleur score
		if score < 5:
			if affichage:
				print("-- Score insuffisant, analyse du second meilleur vote")

			# on stocke la valeur du max, et on le passe à -1, puis on cherche le max
			firstResult = classes[ind]
			firstInd = ind

			classes[ind] = -1 # elimine pour la recherche

			secondResult = 0
			ind = 0

			for i in range(len(classes)):
				if classes[i] > secondResult:
					secondResult = classes[i]
					ind = i

			if affichage:
				print("-- Second meilleur vote: {} avec un vote de {}".format(ind,secondResult))

	if db:
		# on calcule le score, s'il n'est pas concluant, on retourne -1
		score = int(classes[ind]/k*10)
		if affichage:
			print("- Score : {}".format(score))

		if score < 5:
			if affichage:
				print("-- Score insuffisant")
			ind = -1

	# on retourne le chiffre correspond ici à l'indice i
	return ind



## Cross-Validation (Validation Croisée)

def crossValidation_Holdout(img_entrainement, limit = 100):
	"""Evalue la valeur de k, selon la méthode Holdout.
	   limit: valeur maximale que l'on autorise pour k"""

	print("Détermination de k, à l'aide de la validation croisée...")

	tab_recapitulatif = [] # contiendra un tuple par k évalué : [k, nbre_erreurs, pourcentage_erreurs]

	erreurs_k = []

	# on récupère les 2 img: (ici 75 correspond à un pourcentage pour la découpe)
	r = getImagesEntrainement(img_entrainement,75)

	img_ent = r[0] # entrainement
	img_ech = r[1] # echantillon test

	X = len(img_ech[0])
	Y = len(img_ech)

	for k in range(1,limit+1):

		erreurs = 0 	#compteur des erreurs
		total_eval = 0 	# compteur d'images évaluées

		compteur_images = 0

		# on parcourt l'échantillon et on teste la reconnaissance
		for j in range(Y//20):
			for i in range(X//20):
				current_img = getImageAt(img_ech,i,j)	# on récupere l'image à comparer
				result = kNN(current_img, img_ent,k)

				if result != j//5:
					erreurs+=1

				total_eval +=1

				compteur_images +=1
				print("{} échantillons évalués sur {} | {}%".format(compteur_images,150,int((compteur_images/150)*10000)/100))

		pourcentage_erreur = int(((total_eval-erreurs)/total_eval)*10000)/100
		print("K={} | erreurs: {} | pourcentage reconnu: {}%".format(k,erreurs,pourcentage_erreur))
		erreurs_k.append(erreurs)
		tab_recapitulatif.append((k,erreurs,pourcentage_erreur))

	# recherche du k avec le minimum d'erreurs:
	ind = 0
	eMin = erreurs_k[0]

	for i in range(len(erreurs_k)):
		if erreurs_k[i] < eMin:
			eMin = erreurs_k[i]
			ind = i

	return (ind+1,tab_recapitulatif)



## Analyse résultat

def getCaractereForPosition(i,j):
	"""Retourne le caractère pour la position (i,j), cad 0,1,2...
	   i varie de 0 à 99 (100 images/Lignes)
	   j varie de 0 à 49 (50 images/colonnes)
	   Seul j est intéressant ici, pour l'image digits.png"""

	return str(j//5)
