#### Fichier contenant les variables gloables du projet ###
# @author: BOUR Guillaume
# @date: 27-12-2016
# @description: fichier contenant les variables globales utilisees dans le projet
# notamment les paths
#
#
## CONVENTIONS :
# -------------
# Convention de nommage des liens : lien_dossier_{nom_du_dossier}
# A utiliser de la maniere suivante : VariablesGlobales.lien_dossier_{nom_du_dossier}
#
## COMMENTAIRES :
# --------------
#
#

import os
import sys


global lien_dossier_images
global lien_dossier_databases
global lien_dossier_dataset
global lien_dossier_data


sys.path.append(os.path.realpath('..'))

chemin_dossier_app = sys.path[len(sys.path)-1]

lien_dossier_images = "{}/images".format(chemin_dossier_app)
lien_dossier_databases = "{}/data/database".format(chemin_dossier_app)
lien_dossier_dataset = "{}/data/scanSet".format(chemin_dossier_app)
lien_dossier_data = "{}/data".format(chemin_dossier_app)
