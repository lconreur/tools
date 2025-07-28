#!/bin/bash

# Parcourir tous les fichiers commençant par scaffold_
    # Extraire le préfixe avant le premier underscore
    # Nom de base du fichier
    # Nouveau nom : prefix_nom_du_fichier
    # Copier le fichier dans le dossier prefix avec le nouveau nom
	
find . -type f -name 'scaffold_*' | while read -r file; do
    dir=$(basename "$(dirname "$file")")
    prefix=${dir%%_*}
    base=$(basename "$file")
    newname="${prefix}_${base}"
    cp "$file" "prefix/$newname"
done



