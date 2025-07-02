# A quoi sert ce script ?
# Ce script sert à extraire massivement de JGI les fichiers FASTA et GFF issus d'une liste d'organismes identifiés par leur alias.
# Les alias sont listés dans un fichier aliases.txt placés dans le même répertoire que le script.
# Le nom du fichier 'aliases.txt' est inscrit en dur dans le script.

# Input :
# Le fichier d'alias (aliases.txt) dans le même dossier que ce script : un organisme par ligne (ex : Traver1)

# Output :
# Un dossier pour chaque organisme. 
# Dans chaque dossier : 
 # - le fichier gff de JGI correspondant aux gènes : Files/Annotation/Filtered/Genes/GeneCatalog_genes_.gff.gz
 # - le fichier fasta de JGI correspondant aux Assembly Masked : Files/Assembly/(masked)/_AssemblyScaffolds_.fasta.gz

# Exemple pour lire la ligne complète :
# A partir du dossier contenant le script et le fichier aliases.txt :
# python3 recuperer_fichier_JGI_v3.py

import os
import re
import sys
import glob
import subprocess
import datetime
import getpass
import os

username = input("Nom d'utilisateur JGI : ")
password = getpass.getpass("Mot de passe JGI (invisible) : ")

# Authentification initiale à JGI (par ex. en récupérant les cookies)
os.system(f"curl 'https://signon.jgi.doe.gov/signon/create' "
          f"-c cookies -d login={username} -d password={password}")

# === Configuration de l'utilisateur
JGI_USERNAME = username
JGI_PASSWORD = password
ALIASES_FILE = "aliases.txt"

# === Redirection de la sortie vers un fichier log ===
class Tee:
    def __init__(self, *streams):
        self.streams = streams
    def write(self, message):
        for s in self.streams:
            s.write(message)
            s.flush()
    def flush(self):
        for s in self.streams:
            s.flush()

log_filename = f"log_jgi_download_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
log_file = open(log_filename, "w", encoding="utf-8")

sys.stdout = Tee(sys.stdout, log_file)
sys.stderr = Tee(sys.stderr, log_file)

# === Connexion à JGI ===
def create_connection_with_jgi():
    print("Connexion à JGI...")
    os.system(f"curl \"https://signon.jgi.doe.gov/signon/create\" "
              f"--data-urlencode \"login={JGI_USERNAME}\" "
              f"--data-urlencode \"password={JGI_PASSWORD}\" "
              f"-c cookies -s -o /dev/null")
    return os.path.exists("cookies")

# === Téléchargement GFF + FASTA pour un alias ===
def gff_and_fasta_from_alias(alias):
    if not os.path.exists(alias):
        os.makedirs(alias)

    os.system(f"curl 'https://genome.jgi.doe.gov/portal/ext-api/downloads/get-directory?organism={alias}' "
              f"-b ./cookies > ./{alias}/{alias}.xml")

    goodSection = 0
    goodFasta = False
    goodGFF = False
    goodSectionGFF = 0
    goodSectionFasta = 0
    size = 0
    name = False
    url_fasta = ""
    url_gff = ""

    try:
        with open(f"{alias}/{alias}.xml", "r") as file:
            for line in file:
                if line[0] != '<':
                    return False

                if line == '<folder name="Files">\n':
                    goodSection = 1

                if goodSection >= 1:
                    if line.startswith("<folder name=") and line != '<folder name="Files">\n':
                        goodSection += 1
                        if goodSectionGFF >= 1:
                            goodSectionGFF += 1
                        if line == '<folder name="Genome Assembly (masked)">\n':
                            goodFasta = True
                        if line == '<folder name="Genes">\n':
                            goodGFF = True
                        elif line == '<folder name="Filtered Models (&quot;best&quot;)">\n':
                            goodSectionGFF = 1
                    elif line == '</folder>\n':
                        goodSection -= 1
                        if goodSectionGFF >= 1:
                            goodSectionGFF -= 1
                    else:
                        if goodFasta and re.search(r"AssemblyScaffolds.*\.fasta\.gz", line):
                            if not url_fasta:
                                url = line.split("url=\"")[1].split("\"")[0]
                                url_fasta = f"https://genome.jgi.doe.gov/{url}"
                                goodFasta = False
                        elif goodFasta and re.search(r"masked.*\.fasta\.gz", line):
                            if not url_fasta:
                                url = line.split("url=\"")[1].split("\"")[0]
                                url_fasta = f"https://genome.jgi.doe.gov/{url}"
                                goodFasta = False
                        elif goodFasta:
                            if not url_fasta:
                                url = line.split("url=\"")[1].split("\"")[0]
                                url_fasta = f"https://genome.jgi.doe.gov/{url}"
                                goodFasta = False

                        if goodGFF and re.search(r"GeneCatalog_genes_.*\.gff\.gz", line):
                            url = line.split("url=\"")[1].split("\"")[0]
                            url_gff = f"https://genome.jgi.doe.gov/{url}"
                        elif goodGFF and "gff3" in line and "protein" not in line:
                            if not url_gff:
                                url = line.split('url="')[1].split('"')[0]
                                url_gff = f"https://genome.jgi.doe.gov/{url}"
                                goodGFF = False

        if url_fasta:   
            filename_fasta = url_fasta.split("/")[-1]
            os.system(f"curl '{url_fasta}' -b ./cookies > {alias}/{filename_fasta}")
            os.system(f"gunzip -f {alias}/{filename_fasta}")

        if url_gff:
            filename_gff = url.split("/")[-1]
            os.system(f"curl '{url_gff}' -b ./cookies > {alias}/{filename_gff}")

        return True

    except Exception as e:
        print(f"Erreur pour {alias} : {e}")
        return False

# === Script principal ===
if __name__ == "__main__":
    # Nettoyer anciens cookies
    if os.path.exists("cookies"):
        os.remove("cookies")

    # Connexion
    if not create_connection_with_jgi():
        print(" Échec de la connexion à JGI.")
        sys.exit()

    # Vérifier fichier d'alias
    if not os.path.exists(ALIASES_FILE):
        print(" Fichier aliases.txt introuvable.")
        sys.exit()

    # Lire les alias
    with open(ALIASES_FILE) as f:
        aliases = [line.strip() for line in f if line.strip()]

    # Télécharger pour chaque alias
    for alias in aliases:
        print(f"\n>>> Téléchargement pour : {alias}")
        success = gff_and_fasta_from_alias(alias)

        if not success:
            print(f"   Échec ou pas d’accès pour : {alias}")
            continue

    print("\n=== Fin du téléchargement ===")
