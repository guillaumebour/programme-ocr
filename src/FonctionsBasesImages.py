#### Bibliotheque de fonctions pour la gestion d'image ###
# @author: Guillaume Bour
# @date: 28-01-2016
# @description: Fichier regroupant les fonctions de traitement d'image
#
#
# Liste des fonctions implémentées:
#
# # Affichage:
# - affichage
# - affichageGris
# - affichageCoteACote
# - affichageHistogrammeCouleurs
# - affichageHistogrammeGris
# - affichageImageContours
# - contourPourAffichage
#
# # Modifications Couleurs:
# - niveauGris
# - inverseBNImage
# - inversePoints
# - supprimeNoir
# - supprimePetitsContours
#
# # Informations Image:
# - histogrammeCouleurs
# - histogrammeGris
#
# # Seuillage (binarisation -> mod. couleurs..):
# - seuillageSimple
# - seuillageOtsu
#
# # Detection des contours:
# - estDansUnContour
# - joindreListes
# - ajouterAListe
# - nouveauContour
# - nombreVoisinContour
# - nombreVoisinDansContour
# - contoursImage
#
# # Amélioration des contours:
# - getMinMax
# - getNewContours
# - positionRect
# - suppresionContoursInclus
# - getAire
# - getAireMoyenne
# - selectionContoursPetits
# - selectionContoursCaracteres
# - triContoursGaucheDroite
#
# # Extraction des caractères
# - extraitImageContour
# - extraitImagesContours
#
# # Normalisation de l'image
# - transformTo20x20
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
import numpy as np 						# manipulation des images
import matplotlib.pyplot as plt 		# affichage des images
import time 							# calcul du temps d'execution


## FONCTIONS D'AFFICHAGE

def affichage(img):
	"""Affichage d'une image fournie en argument"""
	plt.imshow(img)
	plt.show()


def affichageGris(img):
	"""Affichage d'une image en niveau de gris"""
	plt.imshow(img, cmap='gray')
	plt.show()


def affichageCoteACote(im1, im2):
	"""Affiche 2 images en nuance de gris côte à côte"""
	fig = plt.figure()

	fig.add_subplot(1,2,1)
	plt.imshow(im1, cmap='gray')

	fig.add_subplot(1,2,2)
	plt.imshow(im2, cmap='gray')

	plt.show()


def affichageHistogrammeCouleurs(histogramme):
	"""Affichage de l'histogramme couleurs fourni en argument"""
	X = [i for i in range(256)] # tableau des couleurs de 0 à 255 (absices)

	plt.figure()
	plt.plot(X,histogramme[0],'-r')
	plt.plot(X,histogramme[1],'-g')
	plt.plot(X,histogramme[2],'-b')
	plt.show()


def affichageHistogrammeGris(histogramme):
	"""Affichage de l'histogramme gris fourni en argument"""
	X = [i for i in range(256)] # tableau des couleurs de 0 à 255 (absices)

	plt.figure()
	plt.plot(X,histogramme, '-k')
	plt.show()


def affichageImageContours(image, contours=[], gris = False):
	# image: image en couleurs et non en niveau de gris
	"""Affiche l'image, et superpose les contours."""

	if(gris):
		plt.imshow(image,cmap='gray')
	else:
		plt.imshow(image)

	if not(contours==[]):
		for c in contours:
			r = contourPourAffichage(c)
			X = r[0]
			Y = r[1]
			X.append(c[0][1]) # Permet de former des rectangles au tracé
			Y.append(c[0][0])
			plt.plot(X,Y,'-dr')

	plt.show()


def contourPourAffichage(c):
	"""Retourne la liste des X, et la liste des Y"""
	X, Y = [], []
	for p in c:
		X.append(p[1])
		Y.append(p[0])
	return (X,Y)



## FONCTIONS DE MODIFICATION DES COULEURS

def niveauGris(img):
	"""Retourne l'image en niveau de gris en utilisant la luminance
	L = 299/1000*R+587/1000*G+114/1000*B"""

	start = time.clock()

	print("-- Passage de l'image en niveau de gris...")

	w,h,s = img.shape
	imgGris = np.zeros((w,h))

	for x in range(w):
		for y in range(h):
			imgGris[x,y] = (299/1000)*img[x,y,0] + (587/1000)*img[x,y,1] + (114/1000)*img[x,y,2]

	end = time.clock()

	print("-- Passage en niveau de gris exécuté en {} s".format(int((end-start)*100)/100))
	return imgGris


def inverseBNImage(img):
	"""Inverse les couleurs de l'image: Blanc --> noir | Noir --> blanc"""

	img1 = np.copy(img)

	w,h = len(img1),len(img1[0])

	for x in range(w):
		for y in range(h):
			img1[x][y] = int(not(img[x][y]))

	return img1


def inversePoints(img, tabPts):
	# img : l'image est modifiée directement /!\
	# tabPts: [(x1,y1),(x2,y2),...,(xn,yn)]
	"""Inverse les points de l'image fournis en argument, les passant à leur opposé"""

	for P in tabPts:
		x = P[0]
		y = P[1]
		img[x][y] = int(not(img[x][y]))


def supprimeNoir(img, contour):
	"""Passe les points du contours en blanc"""
	ptHG = [contour[0][1],contour[0][0]]
	ptHD = [contour[3][1],contour[3][0]]
	ptBG = [contour[1][1],contour[1][0]]
	ptBD = [contour[2][1],contour[2][0]]

	# parcours des points du contours
	for x in range(ptHG[0], ptHD[0]+1):
		for y in range(ptHG[1], ptBG[1]+1):
			img[y][x] = 1


def supprimePetitsContours(img, pContours):
	"""Supprime les petits contours de l'image en les passant à la couleur opposée"""
	print("Suppression des petits contours..")

	for c in pContours:
		supprimeNoir(img, c)



## INFORMATIONS SUR L'IMAGE

def histogrammeCouleurs(img):
	"""Retourne 3 tableaux, ordonnées de l'histogramme couleurs"""
	print("Calcul de l'histogramme...")
	YR = [0]*256	# ROUGE
	YG = [0]*256	# VERT
	YB = [0]*256	# BLEU

	w,h,s = img.shape

	for x in range(w):
		for y in range(h):

			# valeurs des pixels RGB [int(val*255)]
			r = int(img[x,y,0]*255)
			g = int(img[x,y,1]*255)
			b = int(img[x,y,2]*255)

			# on incrémente
			YR[r] += 1
			YG[g] += 1
			YB[b] += 1

	return (YR,YG,YB)


def histogrammeGris(img):
	"""Retourne l'histogramme de l'image en niveau de gris"""
	print("-- Calcul de l'histogramme de l'image en niveau de gris...")

	YGr = [0]*256

	w,h = len(img),len(img[0])

	for x in range(w):
		for y in range(h):
			g = int(img[x,y]*255)
			YGr[g] += 1

	return YGr



## SEUILLAGE

def seuillageSimple(img, seuil = 120, inv = False):
	# img : image à fournir
	# seuil : seuil pour le seuillage
	# inv :  False = blanc -> blanc et noir -> noir
	"""Seuillage d'une image en niveau de gris selon un seuil fixé: 120"""

	w,h = len(img), len(img[0])

	binary = np.copy(img)

	for x in range(w):
		for y in range(h):
			pixel = int(binary[x,y]*255)
			if pixel <= seuil:
				binary[x,y] = int(inv)
			else:
				binary[x,y] = int(not(inv))

	print("-- Seuillage de l'image terminé\n")

	return binary


def seuillageOtsu(img, inv = False):
	"""Seuillage d'une image en niveau de gris selon la méthode Otsu"""

	print("-- Seuillage de l'image")

	histo = histogrammeGris(img) # recuperation de l'histogramme

	w,h = len(img), len(img[0])

	totalPixel =  w*h

	somme = 0

	# Calcul de la somme
	for t in range(256):
		somme += t*histo[t]

	sommeB = 0
	wB = 0			# poid background
	wF = 0			# poid foreground

	varMax = 0		# Variation Max
	seuil = 0		# Seuil (renvoyé au final)

	for t in range(256):

		wB += histo[t]

		if wB == 0:
			continue

		wF = totalPixel - wB

		if wF == 0:
			break

		sommeB += t*histo[t]

		mB = sommeB/wB				# Moyenne Background
		mF = (somme - sommeB)/wF	# Moyenne Foreground

		variationEntreClasse = wB*wF*(mB-mF)*(mB-mF) # Calcul de l'écart entre les classes

		# Verification d'un nouveau maximum

		if (variationEntreClasse > varMax):
			varMax = variationEntreClasse
			seuil = t

	print("Seuil détérminé par Otsu: {}".format(seuil))

	return seuillageSimple(img, seuil, inv)



## DETECTION DE CONTOURS

def estDansUnContour(pt, contours):
	"""Retourne l'index si pt (dlf (x,y)) est dans un contour de contours."""
	for contour in contours:
		if pt in contour:
			return contours.index(contour)
	return -1


def joindreListes(i, j, contours):
	"""Join les contours d'indices i et j de contours. Par convention on supprime la liste avec l'indice le plus élevé."""
	"""Modification de 'contours' directement"""
	# Si i et j sont égaux, il n'y a rien à faire
	if not(i == j):
		I,J = min(i,j),max(i,j) 		# on récupère le max
		contours[I] += contours[J] 		# on concatene les 2 contours
		contours.remove(contours[J])	# on supprime le contour J de la liste


def ajouterAListe(elt, i, contours):
	"""Ajoute le point 'elt' au contour i de contours."""
	contours[i].append(elt)


def nouveauContour(elt, contours):
	# elt: dlf (x,y)
	"""Ajoute un contour avec comme unique point elt."""
	contours.append([elt])


def nombreVoisinContour(x, y, img):
	"""Retourne le nombre de points du contour à proximité du point (x,y)"""
	c = 0
	if img[x-1][y-1] == 0:
		c+=1
	if img[x-1][y] == 0:
		c+=1
	if img[x-1][y+1] == 0:
		c+=1
	if img[x][y-1] == 0:
		c+=1
	if img[x][y+1] == 0:
		c+=1
	if img[x+1][y-1] == 0:
		c+=1
	if img[x+1][y] == 0:
		c+=1
	if img[x+1][y+1] == 0:
		c+=1
	return c


def nombreVoisinDansContour(x, y, c):
	"""Retourne la liste des voisins DEJA dans un contour de c"""
	lC = []	#Liste des voisins de (x,y) ds un contour de c

	if not(estDansUnContour((x-1,y),c) == -1):
		lC.append((x-1,y))

	if not(estDansUnContour((x,y-1),c) == -1):
		lC.append((x,y-1))

	if not(estDansUnContour((x,y+1),c) == -1):
		lC.append((x,y+1))

	if not(estDansUnContour((x+1,y),c) == -1):
		lC.append((x+1,y))

	return lC


def contoursImage(image, inv = False):
	"""Retourne une liste des contours de l'image."""
	"""[[(x1,y1),(x2,y2)...], ... ,[(x'1,y'1),...]]"""

	start = time.clock()

	print("-- Détermination des contours...")

	if inv:
		img = inverseBNImage(image)
	else:
		img = np.copy(image)

	contours = [] # Liste des contours

	# On va parcourir l'image en parcourant les colonnes de gauche à droite et de haut en bas

	w,h = len(img),len(img[0])

	for x in range(1,w-1):
		for y in range(1,h-1):
			# Si le pixel est noir, on passe au suivant (ne peux pas appartenir au contour)
			if img[x][y] == 0:
				continue

			cVoisin = nombreVoisinContour(x,y,img)

			# Sinon, on vérifie s'il est au voisinage d'un contour (i.e. d'un pixel noir)
			if cVoisin == 0:
				continue

			# On cherche ensuite le nombre de ses voisins qui sont deja dans un contour:
			listeVoisins = nombreVoisinDansContour(x,y,contours)
			N = len(listeVoisins) # Nombre de voisins dans un contour

			# 3 cas:

			# 1) N == 0 --> on crée un nouveau contour
			if N == 0:
				nouveauContour((x,y),contours)

			# 2) N == 1 --> on ajoute (x,y) au contour qui a un voisin
			elif N == 1:
				indexDuVoisinDansContours = estDansUnContour(listeVoisins[0],contours)
				ajouterAListe((x,y),indexDuVoisinDansContours,contours)

			# 3) Sinon, on fusionne les contours contenant les voisins de (x,y)
			#	 puis on ajoute (x,y) au contour résultant.
			else:

				for p1 in listeVoisins:
					for p2 in listeVoisins:
						i1 = estDansUnContour(p1,contours)			# index du contour contenant p1
						i2 = estDansUnContour(p2,contours)			# index du contour contenant p2
						joindreListes(i1,i2,contours)				# on joint les 2 contours

				i = estDansUnContour(listeVoisins[0],contours)		# index du contour final

				ajouterAListe((x,y),i,contours)						# on ajoute le point

	end = time.clock()

	print("-- Détermination des contours terminée")
	print("Les contours ont été déterminés en {}s\n".format(int((end-start)*100)/100))
	return contours



## Amélioration des contours

def getMinMax(contour):
	"""Retourne le Xmax,Ymax et le Xmin, Ymin d'un contour"""

	X = []
	Y = []

	for p in contour:
		X.append(p[0])
		Y.append(p[1])

	return ((max(X),max(Y)),(min(X),min(Y)))


def getNewContours(contours):
	"""Remplace chaque contour par 4 points (HG, HD, BG, BD)"""
	nouveauContours = []

	for c in contours:
		Max, Min = getMinMax(c)
		HG = (Min[0],Min[1])
		HD = (Max[0],Min[1])
		BG = (Min[0],Max[1])
		BD = (Max[0],Max[1])
		nC = [HG,HD,BD,BG]
		nouveauContours.append(nC)

	return nouveauContours


# Compare la position de 2 rectangles: (1 rect = 1 contour de 4 points)
# Convention:
# 	0 = disjoints
#	1 = collision mais non inclus
# 	2 = inclus
# - - - - - - - - - - - - - - - - - -
# Si 2 non inclu dans 1 et 1 non inclu dans 2 (nécessite donc 2 tests), alors:
#	- soit ils sont disjoints
#	- soit il y a collision
def positionRect(rect_1, rect_2):
	"""Compare la position du rect2 par rapport au rect2 (inclus, disjoint, en collision)\n
	0 = disjoint | 1 = collision mais non inclus | 2 = inclus"""

	ptHG1 = [rect_1[0][1],rect_1[0][0]]
	ptHD1 = [rect_1[3][1],rect_1[3][0]]
	ptBG1 = [rect_1[1][1],rect_1[1][0]]
	ptBD1 = [rect_1[2][1],rect_1[2][0]]

	ptHG2 = [rect_2[0][1],rect_2[0][0]]
	ptHD2 = [rect_2[3][1],rect_2[3][0]]
	ptBG2 = [rect_2[1][1],rect_2[1][0]]
	ptBD2 = [rect_2[2][1],rect_2[2][0]]

	# Test d'inclusion
	if ((ptHG1[0] <= ptHG2[0] <= ptHD2[0] <= ptHD1[0]) and
		(ptHG1[1] <= ptHG2[1] <= ptBG2[1] <= ptBG1[1])):
		 return 2

	# Test d'élimination simple
	elif ((ptHG2[0] > ptHD1[0]) or     	# Trop à Droite
		(ptHD2[0] < ptHG1[0]) or 		# Trop à Gauche
		(ptHG2[1] > ptBG1[1]) or 		# Trop Bas
		(ptBG2[1] < ptHG1[1])):			# Trop Haut
		return 0

	else:
		return 1 # ne permet pas toujours de conclure, exemple: 1 inclus dans 2 retourne "1" !


def suppressionContoursInclus(contours):
	"""Supprime les contours qui sont inclus dans un autre contour."""

	print("Traitement des contours: suppression des contours inclus")

	aSupprimer = []

	# Recherche des contours à supprimer et ajout à une liste
	for i in range(len(contours)):
		for j in range(len(contours)):
			if i!=j and (positionRect(contours[j],contours[i]) == 2):	# i!=j ET contour i inclus dans contour j, on supprime contour i
				aSupprimer.append(i)

	# Suppression des contours inclus
	for i in range(len(contours)-1,0,-1):
		if i in aSupprimer:
			contours.remove(contours[i])

	return contours


def getAire(contour):
	"""Retourne l'aire d'un contour"""
	ptHG = [contour[0][1],contour[0][0]]
	ptHD = [contour[3][1],contour[3][0]]
	ptBG = [contour[1][1],contour[1][0]]
	ptBD = [contour[2][1],contour[2][0]]

	return (ptHD[0]-ptHG[0])*(ptBG[1]-ptHG[1])


def getAireMoyenne(contours):
	"""Retourne l'aire moyenne des contours"""
	somme = 0

	for k in range(len(contours)):
		somme += getAire(contours[k])

	return somme/len(contours)


def selectionContoursPetits(contours, pourcentage = 10):
	"""Retourne un tableau des contours dont l'aire est inférieure à 10/100 de l'aire moyenne."""
	tabContours = []

	aireMoyenne = getAireMoyenne(contours)

	for c in contours:
		if getAire(c) < (pourcentage/100)*aireMoyenne :
			tabContours.append(c)

	return tabContours


def selectionContoursCaracteres(contours, pourcentage = 70):
	"""Retourne un tableau des contours des chiffres (aire> 70/100 de la moyenne)."""
	tabContours = []

	aireMoyenne = getAireMoyenne(contours)

	for c in contours:
		if getAire(c) > (pourcentage/100)*aireMoyenne :
			tabContours.append(c)

	return tabContours


def triContoursGaucheDroite(contours):
	"""Retourne un tableau des contours triés par abscisse de leur sommet gauche croissant"""

	for i in range(len(contours)):
		for j in range(len(contours)):
			x1 = contours[i][0][1]	# x_sommetGauche 1
			x2 = contours[j][0][1]	# x_sommetGauche 2

			if x2 > x1:
				contours[i], contours[j] = contours[j], contours[i] # on échange

	return contours


## Extraction de sous-images

def extraitImageContour(img, contour):
	"""Retourne une image contenant la sous image définie par le contour passé en paramètre."""
	ptHG = [contour[0][1],contour[0][0]]
	ptHD = [contour[3][1],contour[3][0]]
	ptBG = [contour[1][1],contour[1][0]]
	ptBD = [contour[2][1],contour[2][0]]

	debX = ptHG[0]
	finX = ptHD[0]
	debY = ptHG[1]
	finY = ptBG[1]

	return img[debY:finY,debX:finX]


def extraitImagesContours(img, contours):
	"""Retourne un tableau d'images, une par contour."""
	tabImg = []

	for c in contours:
		tabImg.append(extraitImageContour(img,c))

	return tabImg



## NORMALISATION IMAGE

def transformTo20x20(img, newH=20, newL=20, inv = True):
	"""Retourne img avec les dimensions newHxnewL (20x20 par défaut)"""

	# Modification de l'image (on ajoute 20 pixels noir (si inv = True) tout autour)
	Y = len(img)
	X = len(img[0])

	newImage = img

	hauteurImage = len(newImage)
	largeurImage = len(newImage[0])

	hFacteur = hauteurImage//newH
	lFacteur = largeurImage//newL

	nImg = np.zeros([newH,newL])

	for x in range(newL):
		for y in range(newH):
			nImg[y][x] = int(contientPixelContour(newImage,x*lFacteur,y*hFacteur,newL,newH,1,inv))

	return nImg
