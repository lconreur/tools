import os
import re
import sys
import datetime
import getpass
import shutil

# === Configuration ===
# liste d'alias intégrée en dur
organisms = [
    "Abobie1", "Amylap1_1", "Antser1", "Artele1122_1", "Bjead1_1", "Cytmel1", "Daequ1", 
    "Dicsq1", "Earsca1", "Epityp1", "Fibra1", "Fomfom1", "Pipbet1_1", "Ganbon1", 
    "Ganleu1", "Ganluc1", "Gansi1", "Gansp1", "Hexnit1", "Hydfim1", "Irplac1", 
    "Laesu1", "Tralac1", "Tramen1", "Lenti6_1", "Obbri1", "Phaca1", "Phchr2", 
    "Phlbr1", "Phlcen1", "Phlrad1", "Polar1", "Polsqu1", "Porspa1", "PosplRSB12_1", 
    "Pycco1", "Pycpun1", "Fomros1", "Rigmic1", "Trabet1", "Tragib1", "Tralj1", 
    "Tramax1", "Trapol1", "Trapub1", "Traver1"
]

username = input("Nom d'utilisateur JGI : ")
password = getpass.getpass("Mot de passe JGI (invisible) : ")

# === Redirection Log ===
class Tee:
    def __init__(self, *streams): self.streams = streams
    def write(self, m): 
        for s in self.streams: s.write(m); s.flush()
    def flush(self):
        for s in self.streams: s.flush()

log_filename = f"log_jgi_proteins_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
sys.stdout = Tee(sys.stdout, open(log_filename, "w", encoding="utf-8"))

def create_connection_with_jgi():
    print("Connexion à JGI...")
    os.system(f"curl \"https://signon.jgi.doe.gov/signon/create\" "
              f"--data-urlencode \"login={username}\" "
              f"--data-urlencode \"password={password}\" "
              f"-c cookies -s -o /dev/null")
    return os.path.exists("cookies")

def download_proteome_from_alias(alias, target_dir):
    if not os.path.exists(alias):
        os.makedirs(alias)

    # Récupération du XML
    os.system(f"curl 'https://genome.jgi.doe.gov/portal/ext-api/downloads/get-directory?organism={alias}' "
              f"-b ./cookies -s > ./{alias}/{alias}.xml")

    url_protein = ""
    goodSectionFiltered = False

    try:
        if not os.path.exists(f"{alias}/{alias}.xml"):
            return False

        with open(f"{alias}/{alias}.xml", "r") as file:
            for line in file:
                # Priorité à la section Filtered Models
                if 'folder name="Filtered Models (&quot;best&quot;)"' in line:
                    goodSectionFiltered = True
                
                if 'url="' in line and '.fasta.gz' in line and 'protein' in line:
                    url = line.split('url="')[1].split('"')[0]
                    url_protein = f"https://genome.jgi.doe.gov{url}"
                    # Si on est dans la bonne section, on s'arrête, sinon on continue de chercher
                    if goodSectionFiltered:
                        break

        if url_protein:
            filename = f"{alias}.fasta.gz"
            print(f"  Téléchargement : {filename}")
            os.system(f"curl '{url_protein}' -b ./cookies -s > {alias}/{filename}")
            
            # Décompression
            print(f"  Décompression...")
            os.system(f"gunzip -f {alias}/{filename}")
            
            # Copie vers le dossier consolidé pour OrthoFinder
            source_fasta = f"{alias}/{alias}.fasta"
            # Cas où le fichier n'a pas exactement le nom de l'alias après extraction
            extracted_files = [f for f in os.listdir(alias) if f.endswith(".fasta")]
            if extracted_files:
                shutil.copy(f"{alias}/{extracted_files[0]}", f"{target_dir}/{alias}.fasta")
            
            return True
        else:
            print(f"  Erreur : Aucun protéome trouvé pour {alias}")
            return False

    except Exception as e:
        print(f"  Erreur pour {alias} : {e}")
        return False

if __name__ == "__main__":
    # Nettoyage
    if os.path.exists("cookies"): os.remove("cookies")
    
    # Dossier pour OrthoFinder
    consolidated_dir = "PROTEOMES_CONSOLIDATED"
    if not os.path.exists(consolidated_dir):
        os.makedirs(consolidated_dir)

    # Connexion
    if not create_connection_with_jgi():
        print("Échec de la connexion. Vérifiez vos identifiants JGI.")
        sys.exit()

    # Boucle sur les organismes
    for alias in organisms:
        print(f"\n>>> Traitement de : {alias}")
        success = download_proteome_from_alias(alias, consolidated_dir)
        if not success:
            print(f"  [!] Échec pour {alias}")

    print(f"\n=== Terminé ===")
    print(f"Tous les fichiers sont prêts pour OrthoFinder dans le dossier : {consolidated_dir}")