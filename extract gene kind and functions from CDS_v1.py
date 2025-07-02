# Ce fichier extrait les gene_kind et les gene_functions des séquences codantes (CDS) du fichier renseigné dans le prompt.
# Ce fichier fait ensuite le compte par gene_kind et gene_functions.
# Ce fichier doit être placé dans le répertoire dans lequel le fichier se trouve.

from datetime import datetime

from Bio import SeqIO
import os
from collections import Counter

import tkinter as tk
from tkinter import filedialog

# On cache la fenêtre principale de Tkinter
root = tk.Tk()
root.withdraw()

# Ouvre une boîte de dialogue pour choisir un fichier
file_path = filedialog.askopenfilename(
    title="Choisissez un fichier .gbk",
    filetypes=[("Fichiers GenBank", "*.gbk"), ("Tous les fichiers", "*.*")]
)

# Affiche le chemin du fichier sélectionné
if file_path:
    print("Fichier sélectionné :", file_path)
else:
    print("Aucun fichier sélectionné.")

# Chemin vers le fichier .gbk
file_path = file_path #"C:\\Users\\Laurence C\\Documents\\work\\sauvegardelocale\\Daequ1_AssemblyScaffolds_Repeatmasked\\Daaequ1_AssemblyScaffolds_Repeatmasked.gbk"

# Repertoire du fichier
directory = os.path.dirname(file_path)

# Chemin du fichier de log
log_file_path = os.path.join(directory, "extraction_log.txt")

# Compteurs pour gene_kind et gene_function
gene_kind_counter = Counter()
gene_function_counter = Counter()

# Ouvrir le fichier log en mode ajout
with open(log_file_path, "a", encoding="utf-8") as log_file:
    # Ajout du nom du fichier utilisé et de la date/heure
    log_file.write(f"# Fichier analysé : {file_path}\n")
    log_file.write(f"# Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write("=" * 60 + "\n")
    # Ajout de l'entete
    log_file.write("Extraction des informations des CDS avec gene_kind\n")
    log_file.write("=" * 60 + "\n")

    # Lecture de tous les records
    for record in SeqIO.parse(file_path, "genbank"):
        cds_written = False  # pour verifier si on a ecrit au moins 1 CDS dans ce record

        for feature in record.features:
            if feature.type == "CDS" and 'gene_kind' in feature.qualifiers:
                gene_kind = feature.qualifiers['gene_kind'][0]
                gene_kind_counter[gene_kind] += 1

                output_lines = [
                  #  f"CDS: {feature.location}",
                    f"Gene Kind: {gene_kind}"
                ]

                # Traitement facultatif des gene_functions (s’il y en a)
                if 'gene_functions' in feature.qualifiers:
                    gene_functions = feature.qualifiers['gene_functions']
                    gene_function_counter.update(gene_functions)
                    output_lines.append(f"Gene Function(s): {', '.join(gene_functions)}")

                # Écriture dans le log
                if not cds_written:
                    log_file.write(f"\nRecord: {record.id}\n")
                    log_file.write("-" * 60 + "\n")
                    cds_written = True

                log_file.write("\n".join(output_lines) + "\n")
                log_file.write("-" * 60 + "\n")

    # Resume global
    log_file.write("\nResume des gene_kind rencontres :\n")
    for kind, count in gene_kind_counter.items():
        log_file.write(f"  {kind} : {count}\n")

    log_file.write("\nResume des gene_function rencontres :\n")
    for func, count in gene_function_counter.items():
        log_file.write(f"  {func} : {count}\n")

    log_file.write("\nExtraction terminee.\n\n")

print(f"Les resultats ont ete enregistres dans : {log_file_path}")