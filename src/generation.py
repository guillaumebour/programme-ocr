#### Fichier de génération d'un jeu de test ###
# @author: Guillaume Bour
# @date: 28-05-2016
# @description: Fichier de génération d'un jeu de test à partir des scans
#
#
# Liste des fonctions implémentées:
# - extractCaracFromPicture
# - prepareImageTo20x20
# - prepareDataSet
# - getTestImages
# - createTestImage
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


# Importation du module de fonctions
from FonctionsBasesImages import *
from FonctionsReconnaissance import *
import VariablesGlobales

import matplotlib.pyplot as plt
import numpy as np
import os
import random as rd

import cv2

def extractCaracFromPicture(im, affichage = False):
	"""Retourne un tableau des images 20x20 des caractères de l'image pasée en param"""

	# Transformation

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
	nC = selectionContoursCaracteres(nC,10)

	print("Nombre de contours après tri: {}".format(len(nC)))

	# Supprime les impuretés sur l'image de base (améliore la qualité en supprimant les "taches")
	supprimePetitsContours(im, petitsContours)


	if affichage:
		affichageImageContours(imB,nC,True)

	# tri du tableau des contours de gauche à droite
	nC = triContoursGaucheDroite(nC)

	# extraction des caractères
	tabCarac = extraitImagesContours(imB, nC)

	return tabCarac


def prepareImageTo20x20(tabImage, inv = False): # les images recues sont en noires sur fond blanc de base
	"""A partir des caractères, retourne le tableau des images en blanc sur fond noir, en 20x20"""
	"""Unique fonction du programme qui utilise une bibliothèque externe (cv2)"""
	newTab = []

	for image in tabImage:
		newImage = np.zeros((20,20))

		mil = inverseBNImage(cv2.resize(image,(16,16))) # les images recues sont noires sur fond blanc

		if inv:
			mil = inverseBNImage(mil)

		newImage[2:18,2:18] = mil
		newTab.append(newImage)

	return newTab


def prepareDataSet(n, reset = False):
	""" Recupere, formate et sauvegarde le données des fichiers numérisés
		n est le nombre de fichier num_.png"""

	print("Création des jeux de données")
	start = time.clock()

	# Pour chaque chiffre (0-9):
	for c in range(10):
		#on se place dans le repertoire correspondant aux scans de ce chiffre:
		lien_dossier_images = "{}/scan{}".format(VariablesGlobales.lien_dossier_dataset,c)
		os.chdir(lien_dossier_images)

		print("\u25A0 \u25A0 Début des scans pour le chiffre {} \u25A0 \u25A0".format(c))
		print("Répertoire: {}".format(lien_dossier_images))

		# Pour chaque fichier num_.png:
		for k in range(n):

			# on vérifie si les données existent, si oui et que reset est à false, on passe au suivant.
			if os.path.exists("num{}_data.npy".format(k)) and reset == False:
				print("Le fichier num{}_data.npy existe déjà.".format(k))
				continue

			print("Traitement de l'image num{}.png".format(k))

			# on lit l'image et on la traite:
			im = plt.imread("num{}.png".format(k))

			# on récupère les chiffres de l'image
			tab = extractCaracFromPicture(im)

			# On formate
			images = prepareImageTo20x20(tab)

			# On sauvegarde
			np.save("num{}_data.npy".format(k), images)
			print("Sauvegarde effectuée ! Fichier : num{}_data.npy".format(k))
			print("L'image num{}.png a été traitée avec succès\n".format(k))

		print("\u25A0 \u25A0 Traitement du chiffre {} terminé \u25A0 \u25A0\n".format(c))

	end = time.clock()

	print("Le traitement du jeu d'entrainement a été effectué en {}s".format(int((end-start)*100)/100))


def getTestImages(n, reset = False):
	"""Crée un tableau de toutes les images de tous les chiffres
		n : nombre d'image num_.png par caractères
		reset: force le programme à regénerer toutes les images même si les fichiers existent déjà.
		"""

	# Prepare le jeu de données si pas déjà fait
	prepareDataSet(n, reset)

	print("Création du tableau de toutes les images")
	# On doit récupérer toutes les sous-images stockées dans les fichiers

	tabImages = [] # va contenir toutes les images

	# Pour chaque chiffre:
	for c in range(10):

		tabC = [] # tableau qui va contenir tous les 0 ou tous les 1 etc...

		# on se place dans le bon répertoire:
		lien_dossier_images = "{}/scan{}".format(VariablesGlobales.lien_dossier_dataset,c)
		os.chdir(lien_dossier_images)

		# pour chaque fichier num, on charge le tableau correspondant et on ajoute tous les chiffres
		for k in range(n):

			# on charge les données
			tmp_tab = np.load("num{}_data.npy".format(k))

			# on copie les données dans tabC

			for i in tmp_tab:
				tabC.append(i)

		print("Nombre d'images pour {} : {}".format(c,len(tabC)))

		# on ajoute tabC à tabImages
		tabImages.append(tabC)

	# On sauvegarde le tableau dans Jeu_Test:
	os.chdir(VariablesGlobales.lien_dossier_dataset)

	np.save("images_test_data.npy",tabImages)

	return tabImages


def createTestImage(n, reset = False):
	"""Crée l'image de test
		n : nombre de num par chiffre
		reset: ne prend pas en compte les fichiers existants"""

	# on récupère le tableau des images, s'il n'existe pas il est crée
	os.chdir(VariablesGlobales.lien_dossier_dataset)

	tabImages = []

	if reset:
		print("Reset du jeu de données")

	if not(os.path.exists("images_test_data.npy")) or reset == True:
		tabImages = getTestImages(n,reset)
	else:
		tabImages = np.load("images_test_data.npy")


	# Vérification des dimensions des tableaux pour chaque chiffre:
	taille_ref = len(tabImages[0])

	for tab in tabImages:
		if len(tab) != taille_ref:
			print("[ERREUR] : les tailles ne correspondent pas : {} =|= {}".format(len(tab),taille_ref))
			return

	# Si les dimensions sont correctes, on calcule le nombre d'images par lignes (pour 5 lignes)
	nbre_images_lignes = taille_ref//5 # ds le cas ou ce n'est pas un multiple, on laisse des images de cotes

	# l'image est crée: de taille 20*nbre_images_lignes sur 20*5*10
	image_finale = np.zeros((10*5*20,nbre_images_lignes*20))

	# on remplie l'image au fur et à mesure, pouur chaque caractère:
	for carac in range(10):
		c = 0 			# compteur d'image incluse (correspond aussi à la colonne avec un modulo nbre_images_lignes)
		i = carac*5*20 		# compteur de la ligne (ici en pixels déjà)
		l = 0 			# compteur de lignes déja ecrites

		# tant qu'il reste des images dans le tableau
		while c < taille_ref:
			image_finale[i:i+20,(c%nbre_images_lignes)*20:(c%nbre_images_lignes)*20+20] = tabImages[carac][c]
			c+=1 # on augmente le compteur, puisqu'une image a été ajouté

			# il faut vérifier si on oit changer de ligne:
			if c//nbre_images_lignes > l:
				l+=1
				i+=20

	image_finale = 255*image_finale # car constituée de 0 et de 1...

	cv2.imwrite("image_test.png",image_finale)

	return image_finale
