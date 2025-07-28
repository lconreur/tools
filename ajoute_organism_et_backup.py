import os
import shutil

# Dossier du script
folder = os.path.dirname(os.path.abspath(__file__))

# Parcours de tous les fichiers .gbk
for filename in os.listdir(folder):
    if filename.endswith(".gbk"):
        filepath = os.path.join(folder, filename)
        backup_path = filepath + ".bak"
        new_organism = filename.split('_')[0]

        # Créer une copie de sauvegarde
        shutil.copy2(filepath, backup_path)

        # Lire le contenu du fichier
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Modifier la ligne "ORGANISM"
        new_lines = []
        for line in lines:
            if line.strip().startswith("ORGANISM"):
                line = "  ORGANISM  " + new_organism + "\n"
            new_lines.append(line)

        # Écrire le nouveau contenu dans le fichier original
        with open(filepath, 'w') as f:
            f.writelines(new_lines)

        print(f"Modifie : {filename} => ORGANISM = {new_organism} (sauvegarde: {filename}.bak)")
