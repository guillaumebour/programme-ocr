#### Bibliotheque de fonctions pour l'intéraction avec une base de données ###
# @author: Guillaume Bour
# @date: 23-05-2016
# @description: Fichier regroupant les fonctions pour l'intéraction avec une base de données
#
#
# Liste des fonctions implémentées:
#
# # CREATION DE LA DB
# - createDatabaseIfNotExists
# - checkForTableExistence
#
# # INTERACTION AVEC LA DB
# - executeQueryOnDB
# - getInfosForCode
# - getLikeData
#
#
## COMMENTAIRES :
# --------------
#
#


# MODULES NECESSAIRES
import sqlite3
import os
import sys

import VariablesGlobales	# Chemin d'accès aux fichiers



## CREATION DE LA BASE DE DONNEES

def createDatabaseIfNotExists():
	"""Crée le fichier sqlite, et insere les données dans la table"""

	os.chdir(VariablesGlobales.lien_dossier_databases)

	# ouverture de la base
	db = sqlite3.connect("France.db")
	cursor = db.cursor()

	if not(checkForTableExistence("France","villes_francaises")):
		print("La table '{}' n'existe pas. Création de la table {}".format("villes_francaises","villes_francaises"))
		query = '''CREATE TABLE IF NOT EXISTS villes_francaises(id INTEGER PRIMARY KEY, nom_commune TEXT, code_commune_INSEE TEXT, code_postal TEXT, libelle_acheminement TEXT, ligne_5 TEXT);'''
		cursor.execute(query)
		db.commit()
	else:
		print("La table {} existe déjà dans la base.".format('villes_francaises'))

	# On vérifie si la table villes francaises contient des données.
	query = "SELECT count(*) FROM villes_francaises;"
	cursor.execute(query)
	db.commit()
	result = cursor.fetchone()

	if result[0] == 0:
		print("La table villes_françaises est vide. Remplissage de la table...")

		# Ouverture du fichier .csv en lecture
		fichier_csv = open("laposte_hexasmal.csv","r")

		villes = []
		i = 0 # compteur

		for ligne in fichier_csv:
			if i != 0:
				tmp = ligne.split(";")							# on découpe suivant ';'
				v = (i-1,tmp[1],tmp[0],tmp[2],tmp[3],tmp[4])	# on récupère les infos dans un tuple
				villes.append(v)								# on ajoute aux villes
			i += 1

		fichier_csv.close()

		# ajout des données:
		cursor.executemany('''INSERT INTO villes_francaises VALUES(?,?,?,?,?,?);''',villes)
		db.commit()


	else:
		print("La table villes_françaises contient déjà des données.\nActuellement {} entrées.".format(result[0]))


	# fermeture de la base
	db.close()


def checkForTableExistence(db_name, table_name):
	"""Vérifie si la table existe dans la base True = existence"""

	os.chdir(VariablesGlobales.lien_dossier_databases)

	db= sqlite3.connect("{}.db".format(db_name))
	cursor = db.cursor()

	query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table_name)

	cursor.execute(query)
	db.commit()

	result = cursor.fetchone()

	db.close()

	return result



## INTERACTION AVEC LA DB

def executeQueryOnDB(query):
	"""Execute la requete sur la db"""

	os.chdir(VariablesGlobales.lien_dossier_databases)

	db= sqlite3.connect("France.db")
	cursor = db.cursor()

	cursor.execute(query)
	db.commit()

	r = cursor.fetchall()

	db.close()

	return r


def getInfosForCode(code_postal):
	"""Retourne une chaine de caractère avec les infos des villes correspondants au code postal"""

	print("Recherche d'informations pour le code postal {}...".format(code_postal))
	query = '''SELECT * FROM villes_francaises WHERE code_postal = {};'''.format(code_postal)

	result = executeQueryOnDB(query)

	tabVillesInfos = []

	for ville in result:
		if ville[5]=="\n":
			str = "Commune: {}\nNuméro INSEE: {}\nCode postal: {}\nLibellé: {}  {}".format(ville[1],ville[2],ville[3],ville[4],ville[5])
		else:
			str = "Commune: {}\nNuméro INSEE: {}\nCode postal: {}\nLibellé: {} - {}".format(ville[1],ville[2],ville[3],ville[4],ville[5])
		tabVillesInfos.append(str)

	print("Recherche terminée\n")
	return tabVillesInfos


def getLikeData(pattern):
	"""Retourne les codes postaux ayant le pattern passé en paramêtre (ex: 57%70)..."""
	query = '''SELECT DISTINCT code_postal FROM villes_francaises WHERE code_postal LIKE "{}";'''.format(pattern)

	return executeQueryOnDB(query)



## CODE D INITIALISATION

print("\n-- Initialisation BDD...")
createDatabaseIfNotExists()
print("-- Initialisation BDD terminée.\n")
