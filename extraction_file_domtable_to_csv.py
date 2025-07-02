import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Bio import SearchIO

# 🪟 Interface graphique silencieuse
root = tk.Tk()
root.withdraw()

# ✅ Demande à l'utilisateur s'il veut traiter 1 fichier ou un dossier complet
response = messagebox.askyesno(
    title="Choix du mode",
    message="Voulez-vous traiter TOUS les fichiers d'un répertoire ?\n\n"
            "👉 Oui = traiter un dossier\n"
            "👉 Non = traiter un seul fichier"
)

files_to_process = []

if response:  # ✅ Mode dossier
    folder_path = filedialog.askdirectory(title="Sélectionner un dossier")
    if not folder_path:
        print("Aucun dossier sélectionné. Fin du script.")
        exit()
    # Prendre tous les fichiers avec extensions connues
    for file in os.listdir(folder_path):
        if file.endswith((".domtable", ".domtblout", ".txt", ".out")):
            files_to_process.append(os.path.join(folder_path, file))
else:  # ✅ Mode fichier unique
    file_path = filedialog.askopenfilename(
        title="Sélectionner un fichier .domtable ou .domtblout",
        filetypes=[("Fichiers HMMER DOMTAB", "*.domtable *.domtblout *.txt *.out"), ("Tous les fichiers", "*.*")]
    )
    if not file_path:
        print("Aucun fichier sélectionné. Fin du script.")
        exit()
    files_to_process.append(file_path)

# Définir le dossier de sortie (celui du premier fichier)
output_dir = os.path.dirname(files_to_process[0])
output_file = os.path.join(output_dir, "output_file.csv")

# En-têtes du fichier CSV
csv_headers = [
    "source_file",  # <--- nom du fichier source
    "query_id", "query_length",
    "hit_id", "hit_description", "hit_length", "hit_evalue", "hit_bitscore",
    "hsp_evalue", "hsp_bitscore", "hsp_bias",
    "query_start", "query_end",
    "hit_start", "hit_end"
]

# Traitement + écriture dans UN SEUL fichier CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_headers)

    for input_file in files_to_process:
        print(f"🔍 Traitement : {input_file}")
        try:
            for record in SearchIO.parse(input_file, "hmmsearch3-domtab"):
                for hit in record.hits:
                    for hsp in hit.hsps:
                        writer.writerow([
                            os.path.basename(input_file),  # nom du fichier source
                            record.id,
                            record.seq_len,
                            hit.id,
                            hit.description,
                            hit.seq_len,
                            hit.evalue,
                            hit.bitscore,
                            hsp.evalue,
                            hsp.bitscore,
                            hsp.bias,
                            hsp.query_start,
                            hsp.query_end,
                            hsp.hit_start,
                            hsp.hit_end
                        ])
        except Exception as e:
            print(f"❌ Erreur dans le fichier {input_file} : {e}")

print(f"\n✅ Tous les résultats ont été exportés dans :\n{output_file}")
