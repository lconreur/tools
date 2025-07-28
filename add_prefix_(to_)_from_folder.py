# Ce script ajoute un préfixe aux noms de fichiers contenant ".region". Le préfixe est défini par les caractères avant le premier _ du répertoire contenant le fichier.
# Ce script crée un fichier de log indiquant le nombre de fichiers renommés, leur nom initial et leur nouveau nom.
# Si le script est lancé une deuxième fois, le fichier de log est cumulatif.
# Ce script s'applique aux fichiers présents dans le même répertoire que lui et dans ses sous-répertoires.

import os
import shutil
from datetime import datetime

# Répertoire où se trouve le script
racine_script = os.path.dirname(os.path.abspath(__file__))

# Dossier de destination pour les fichiers renommés
dossier_renomme = os.path.join(racine_script, "renomme")
os.makedirs(dossier_renomme, exist_ok=True)

# Liste pour journalisation
fichiers_renommes = []

# Parcours récursif de tous les fichiers dans les sous-dossiers
for dossier_courant, _, fichiers in os.walk(racine_script):
    # Ignorer le dossier "renomme" lui-même
    if os.path.abspath(dossier_courant) == os.path.abspath(dossier_renomme):
        continue

    # Préfixe = partie avant le premier underscore du dossier
    nom_dossier = os.path.basename(dossier_courant)
    if "_" not in nom_dossier:
        continue  # ignorer les dossiers sans underscore
    prefixe = nom_dossier.split("_", 1)[0] + "_"

    for nom_fichier in fichiers:
        if ".region" in nom_fichier.lower():
            chemin_original = os.path.join(dossier_courant, nom_fichier)

            # Ne pas renommer s’il commence déjà par le préfixe
            if not nom_fichier.startswith(prefixe):
                nouveau_nom = prefixe + nom_fichier
                chemin_nouveau = os.path.join(dossier_courant, nouveau_nom)

                # Renommer
                os.rename(chemin_original, chemin_nouveau)
                fichiers_renommes.append((chemin_original, chemin_nouveau))

                # Copier vers le dossier "renomme"
                chemin_destination = os.path.join(dossier_renomme, nouveau_nom)
                shutil.copy2(chemin_nouveau, chemin_destination)

# Journalisation (en mode ajout)
log_path = os.path.join(racine_script, "log_renommage.txt")
with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write(f"\n---\nJournal de renommage - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write(f"Nombre total de fichiers renommés : {len(fichiers_renommes)}\n")

    for ancien, nouveau in fichiers_renommes:
        log_file.write(f"{ancien} → {nouveau}\n")

print(f"{len(fichiers_renommes)} fichier(s) renommé(s) et copiés dans 'renomme/'.")
print("Log mis à jour dans 'log_renommage.txt'")
