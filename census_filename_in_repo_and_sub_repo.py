import os
import csv

# Dossier à explorer
racine = "C:/Users/Laurence C/Documents/genomes/"

# Fichier de sortie
csv_path = "fichiers_recenses.csv"

with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["chemin_complet", "dossier_contenant", "fichier_fasta", "fichier_gff"])

    for root, dirs, files in os.walk(racine):
        fasta_file = ""
        gff_file = ""
        
        for file in files:
            if "fasta" in file.lower() and not fasta_file:
                fasta_file = file
            if "gff" in file.lower() and not gff_file:
                gff_file = file
        
        # Écrit une ligne seulement s'il y a au moins un fichier d'intérêt
        if fasta_file or gff_file:
            chemin_complet = os.path.join(root)
            dossier_contenant = os.path.basename(root)
            writer.writerow([chemin_complet, dossier_contenant, fasta_file, gff_file])
            
print(f" Fichier CSV créé : {csv_path}")