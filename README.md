Ceci est mon premier fichier README. Ce répertoire contient les outils développés au fur et à mesure de mes besoins.

# tools
# add prefix (3digits) from folder.py
Ce script ajoute un préfixe aux noms de fichiers contenant ".region". Le préfixe est défini par les 3 premiers caractères du répertoire contenant le fichier.
Ce script crée un fichier de log indiquant le nombre de fichiers renommés, leur nom initial et leur nouveau nom.
Si le script est lancé une deuxième fois, le fichier de log est cumulatif.
Ce script s'applique aux fichiers présents dans le même répertoire que lui et dans ses sous-répertoires.

# extraction gene kind and functions from CDS_v1.py
Ce script extrait les gene_kind et les gene_functions des séquences codantes (CDS) du fichier .gbk renseigné dans le prompt.
Ce script fait ensuite le compte par gene_kind et gene_functions.
Ce script créera le fichier de log dans lequel le fichier se trouve, avec l’information du fichier analysé et un timestamp.
Si le script est lancé une deuxième fois, le fichier de log est cumulatif.

# extraction_file_domtable_to_csv.py
Ce script demande à l’uilisateur s’il veut extraire les infos de tous les fichiers .domtable d’un répertoire ou un seul fichier.
A partir de là il va extraire les données suivantes et les insérer dans un fichier .csv dans le répertoire choisi.
source_file
query_id
query_length
hit_id
hit_description
hit_length
hit_evalue
hit_bitscore
hsp_evalue
hsp_bitscore
hsp_bias
query_start
query_end
hit_start
hit_end

# recuperer_fichier_JGI_vdef.py
Ce script sert à extraire massivement de JGI les fichiers FASTA et GFF issus d'une liste d'organismes identifiés par leur alias.
Les alias sont listés dans un fichier aliases.txt placés dans le même répertoire que le script.
Le nom du fichier 'aliases.txt' est inscrit en dur dans le script.

Input :
Le fichier d'alias (aliases.txt) dans le même dossier que ce script : un organisme par ligne (ex : Traver1)

Output :
Un dossier pour chaque organisme. 
Dans chaque dossier : 
 - le fichier gff de JGI correspondant aux gènes : Files/Annotation/Filtered/Genes/GeneCatalog_genes_.gff.gz
 - le fichier fasta de JGI correspondant aux Assembly Masked : Files/Assembly/(masked)/_AssemblyScaffolds_.fasta.gz

Exemple pour lire la ligne complète :
A partir du dossier contenant le script et le fichier aliases.txt :
python3 recuperer_fichier_JGI_vdef.py
