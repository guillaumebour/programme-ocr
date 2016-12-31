#/bin/sh

# name : clean_project.sh
# date : 26/12/16
# author : Guillaume Bour

# This script removes all files generated during execution
# This includes :
# - *.npy files in data/dataSet/scan* directories
# - *.db file in database directory

function supprime_fichier
{
  for file in "$@"
  do
    if [ -f $file ]
    then
      rm $file
    fi
  done
}
DOSSIER=$(dirname $(readlink -f $0));

echo $DOSSIER

cd $DOSSIER

# DATABASE
cd "../data"
echo "cleaning `pwd`..."

supprime_fichier "crossValidationHoldoutResult.txt"

# DATABASE
cd "database"
echo "cleaning `pwd`..."

supprime_fichier "France.db"

# SCANSET
cd "../scanSet"
echo "cleaning `pwd`..."

supprime_fichier *.npy
supprime_fichier "image_test.png"

for i in `seq 0 9`;
do
  cd "scan$i"
  supprime_fichier *.npy
  cd ".."
done

echo "Project has been cleaned !"
