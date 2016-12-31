#### Fichier d'exécution ###
# @author: BOUR Guillaume
# @date: 26-05-2016
# @description: fichier d'execution du programme
#
#
#
#
# Liste des fonctions implémentées:
#
# # Extraction Des Contours
# - extractionCaracteres
# - normaliseTabImages
#
# # Reconnaissance
# - kNNrecognition
# - determination_k
#
# # Code Principal
# - reconnaissance
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


import VariablesGlobales

from FonctionsBasesImages import *
from FonctionsReconnaissance import *
from FonctionsBDD import *
from generation import *

import matplotlib.pyplot as plt
import numpy as np
import os
import random as rd


## EXTRACTION DES CONTOURS

def extractionCaracteres(im, affichage = False):
	"""Retourne un tableau contenant les sous-images des caractères de l'image"""

	# Passage de l'image en niveau de gris
	imG = niveauGris(im)

	# Passage de l'image en noir et blanc uniquement
	imB = seuillageOtsu(imG)

	# Récupération des contours
	c = contoursImage(imB)

	# Transformation des contours en contours rectangulaires
	nC = getNewContours(c)

	print("Nombre de contours détectés: {}".format(len(nC)))

	# Selectionne les petits contours
	petitsContours = selectionContoursPetits(nC,5)

	# Supprime les contours inclus (cas pour 0,2,6,8,9...)
	nC = suppressionContoursInclus(nC)

	# Selectionne les caractères uniquement ( aire > 20%)
	nC = selectionContoursCaracteres(nC,20)

	print("Nombre de contours après tri: {}".format(len(nC)))

	# Supprime les impuretés sur l'image de base (améliore la qualité en supprimant les "taches")
	supprimePetitsContours(im, petitsContours)

	if affichage:
		affichageImageContours(imB,nC,True)

	# triage du tableau des contours de gauche à droite
	nC = triContoursGaucheDroite(nC)

	# extraction des caractères
	tabCarac = extraitImagesContours(imB, nC)

	for i in range(len(tabCarac)):
		tabCarac[i] = inverseBNImage(tabCarac[i])


	return tabCarac


def normaliseTabImages(tabImage):
	"""transforme en 20x20"""

	for i in range(len(tabImage)):
		tabImage[i] = transformTo20x20(tabImage[i])

	return tabImage



## RECONNAISSANCE

def kNNrecognition(digits, im_ent, k, aff=False, scores = True, db = True):
	"""Retourne le tableau apres reconnaissance"""

	print("\n-- Reconnaissance avec la méthode des k plus proches voisins (k={})...".format(k))
	start = time.clock()

	result = []
	c = 0
	t = len(digits)

	for image in digits:
		result.append(kNN(image,im_ent,k,affichage=aff, scores = scores, db = db))
		c+=1
		print("{}% effectué".format(c/t*100))

	if -1 in result:

		print("Le résultat n'est pas certain, recherche des codes postaux probables avec la base de données")
		pattern = ""

		for car in result:
			if car == -1:
				pattern+="_"
			else:
				pattern+=str(car)

		codesPostauxProbables = getLikeData(pattern)

		if len(codesPostauxProbables) != 0:
			print("{} codes postaux correspondants:".format(len(codesPostauxProbables)))
		else:
			print("Aucune correspondance")

		for cp in codesPostauxProbables:
			print(cp[0])

	end = time.clock()

	print("La reconnaissance a été effectuée en {}s".format(int((end-start)*100)/100))
	print("-- Reconnaissance avec la méthode des k plus proches voisins terminée\n")

	return result


def determination_k():

	os.chdir(VariablesGlobales.lien_dossier_dataset)

	im = plt.imread('image_test.png')

	r = crossValidation_Holdout(im,limit = 60)

	print("Valeur optimale pour k : {}".format(r[0]))
	print("Ecriture des résultats dans un tableau")

	os.chdir(VariablesGlobales.lien_dossier_data)

	fichier = open("crossValidationHoldoutResult.txt","w+")

	result = r[1]

	for k in range(len(result)):

		fichier.write("{}\t{}\t{}\n".format(result[k][0],result[k][1],result[k][2])) # k | erreurs | pourcentage d'erreur

	fichier.close()



## CODE PRINCIPAL

def reconnaissance(affichage = False, database = True, scores = True):

	os.chdir(VariablesGlobales.lien_dossier_dataset)

	if not os.path.isfile('image_test.png'):
		print("image_test.png not found")
		print("Creating image_test.png...")
		createTestImage(3)
		os.chdir(VariablesGlobales.lien_dossier_dataset)

	im2 = plt.imread('image_test.png')

	os.chdir(VariablesGlobales.lien_dossier_images)

	# image a reconnaitre dans le dossier images
	im = plt.imread('code_postal_73620.png')

	tab = extractionCaracteres(im, affichage=False)
	tab = prepareImageTo20x20(tab, True)

	result = kNNrecognition(tab,im2,5,aff = affichage, scores = scores, db = database)

	str_code = ""
	for c in result:
		str_code+=str(c)

	print("Code postal reconnu: {}\n".format(str_code))

	infos = getInfosForCode(str_code)

	print("Résultats de la recherche:\n")
	print("----------------------------------------")

	if(infos):
		for i in infos:
			print(i)
			print("----------------------------------------")
	else:
		print("La recherche n'a donné aucun résultat")

	print("\nProgramme terminé")



## EXECUTION

#determination_k() # /!\ Execution tres longue ! cf dossier "results"

# Parametres generaux
affichage_intermediaire = False
utilisation_bdd = False
utilisation_scores = True


reconnaissance(affichage_intermediaire, utilisation_bdd, utilisation_scores)
