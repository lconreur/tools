import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Bio import Phylo

# --- 1. CONFIGURATION VISUELLE ---
plt.rcParams['lines.linewidth'] = 1.5  # Arbre fin pour la clarté

# --- 2. CHARGEMENT DES DONNÉES ---
tree = Phylo.read("arbre_final.nwk", "newick")
leaf_names = [leaf.name for leaf in tree.get_terminals()]

# /!\ CHANGEMENT DE FICHIER ICI /!\
file_name = 'données pour arbre phylogénétique_clacla_2.xlsx' 
try:
    df_raw = pd.read_excel(file_name)
except FileNotFoundError:
    print(f"Erreur : Le fichier '{file_name}' est introuvable.")
    exit()

df = df_raw[df_raw['Nom'].isin(leaf_names)].copy()
missing = set(leaf_names) - set(df_raw['Nom'].unique())
print(f"Organismes dans l'arbre mais PAS dans l'Excel : {missing}")
df = df.set_index('Nom').reindex(leaf_names).reset_index()

# Couleurs par Clade (tab20)
unique_clades = df['Clade'].unique()
cmap = plt.cm.get_cmap('tab20', len(unique_clades))
clade_color_map = {clade: cmap(i) for i, clade in enumerate(unique_clades)}

# --- 3. CALCUL DES POSITIONS GÉOMÉTRIQUES ---
def get_x_positions(tree):
    positions = {tree.root: 0}
    for clade in tree.get_nonterminals():
        for child in clade:
            dist = child.branch_length if child.branch_length is not None else 0.1
            positions[child] = positions[clade] + dist
    return positions

def get_y_positions(tree):
    return {leaf: i + 1.5 for i, leaf in enumerate(tree.get_terminals())}

x_pos = get_x_positions(tree)
y_pos = get_y_positions(tree)

def fill_internal_y(clade):
    if clade.is_terminal(): return y_pos[clade]
    child_ys = [fill_internal_y(c) for c in clade]
    y_pos[clade] = sum(child_ys) / len(child_ys)
    return y_pos[clade]

fill_internal_y(tree.root)
max_x = max(x_pos.values())

# --- 4. CRÉATION DE LA FIGURE ---
# /!\ AJUSTEMENT DES RATIOS : Le tableau est plus large /!\
fig, (ax_tree, ax_table, ax_chart) = plt.subplots(1, 3, figsize=(36, 22), 
                                                 gridspec_kw={'width_ratios': [0.5, 1.4, 1.1]})

# --- A. TRACÉ DE L'ARBRE ---
for clade in tree.find_clades():
    x_p, y_p = x_pos[clade], y_pos[clade]
    if not clade.is_terminal():
        child_ys = [y_pos[c] for c in clade]
        ax_tree.plot([x_p, x_p], [min(child_ys), max(child_ys)], color='black')
        for child in clade:
            ax_tree.plot([x_p, x_pos[child]], [y_pos[child], y_pos[child]], color='black')

for leaf in tree.get_terminals():
    ax_tree.plot([x_pos[leaf], max_x], [y_pos[leaf], y_pos[leaf]], color='black', linestyle=':')

ax_tree.set_ylim(0, len(df) + 1)
ax_tree.invert_yaxis()
ax_tree.axis('off')

# --- B. LE TABLEAU (AVEC NOUVELLE COLONNE FUNGAL-RIPP) ---
ax_table.axis('off')
df_display = df.copy()
df_display['Genome Assembly size (Mbp)'] = df_display['Genome Assembly size (Mbp)'].map('{:.2f}'.format)
# Attention au nom de colonne exact dans le nouveau fichier
col_total_bgc = 'Nombre total de BGC sans tprec, indole et betalactone)'
if col_total_bgc not in df_display.columns: col_total_bgc = 'Nombre total de BGC' # Sécurité

df_display['Nombre de BGC par Mb'] = df_display['Nombre de BGC par Mb'].map('{:.2f}'.format)

# Ajout de la colonne Fungal-RiPP dans les données affichées
table_data = df_display[['Clade', 'Nom', 'Genome Assembly size (Mbp)', col_total_bgc, 'Nombre de BGC par Mb', 'Nombre de fungal-RiPP']].values
# Nouveaux labels d'en-tête
table_labels = ['Clade', 'Organisme', 'Taille (Mbp)', 'Total BGC', 'BGC / Mb', 'RiPP']

the_table = ax_table.table(
    cellText=table_data, 
    colLabels=table_labels, 
    loc='center', 
    bbox=[0, 0, 1, 1],
    cellLoc='center'
)

the_table.auto_set_font_size(False)
the_table.set_fontsize(11)

# /!\ AJUSTEMENT LARGEUR COLONNES : pour 6 colonnes /!\
col_widths = [0.15, 0.38, 0.12, 0.11, 0.14, 0.10]

for (row, col), cell in the_table.get_celld().items():
    cell.set_width(col_widths[col])
    cell.set_height(1 / (len(df) + 1))
    cell.set_edgecolor('#D3D3D3') # Bordures grises douces
    
    if row == 0:
        cell.set_facecolor('#4F4F4F')
        cell.get_text().set_color('white')
        cell.get_text().set_weight('bold')
    else:
        clade_name = df.iloc[row-1]['Clade']
        color = clade_color_map[clade_name]
        
        # Style pour Clade (0) et Organisme (1)
        if col == 0: cell.get_text().set_color(color); cell.get_text().set_weight('bold')
        elif col == 1: cell.get_text().set_color(color); cell.get_text().set_weight('bold'); cell.get_text().set_style('italic')
        else: cell.get_text().set_color('black') # Chiffres en noir

# --- C. L'HISTOGRAMME (AVEC FUNGAL-RIPP ET DÉCALAGE "FANTÔME") ---
# 1. Extraction des données
terp = df['Nombre de terpènes (sans les précursors)'].values
nrps = df['Nombre de NRPS et NRPS-like'].values
pks  = df['Nombre de PKS (I et III)'].values
ripp = df['Nombre de fungal-RiPP'].values # Nouvelle catégorie !

# /!\ Insertion du 0 au début pour avoir les histogrammes alignés en face du reste /!\
terp_shifted = np.insert(terp, 0, 0)
nrps_shifted = np.insert(nrps, 0, 0)
pks_shifted  = np.insert(pks, 0, 0)
ripp_shifted = np.insert(ripp, 0, 0) # On décale aussi le RiPP

# Positions Y décalées (pour l'en-tête)
pos_shifted = np.arange(len(df) + 1) + 0.5

h_bars = 0.6

# 2. COULEURS PASTEL SYNCHRONISÉES
color_terp = "#C5C5B8"  # Gris-beige
color_nrps = "#AEC7E8"  # Bleu ciel
color_pks  = "#FFB3B3"  # Corail/rosé
color_ripp = "#CAFFBF"  # Vert menthe (fungal-RiPP)

# 3. Tracé des barres cumulées (stacked)
# Les bases de l'empilement changent : terp -> terp+nrps -> terp+nrps+pks
ax_chart.barh(pos_shifted, terp_shifted, h_bars, color=color_terp, edgecolor='black', linewidth=0.5, label='Terpènes')
ax_chart.barh(pos_shifted, nrps_shifted, h_bars, left=terp_shifted, color=color_nrps, edgecolor='black', linewidth=0.5, label='NRPS + like')
ax_chart.barh(pos_shifted, pks_shifted,  h_bars, left=terp_shifted+nrps_shifted, color=color_pks, edgecolor='black', linewidth=0.5, label='PKS (I & III)')
ax_chart.barh(pos_shifted, ripp_shifted, h_bars, left=terp_shifted+nrps_shifted+pks_shifted, color=color_ripp, edgecolor='black', linewidth=0.5, label='fungal-RiPP')

# 4. Chiffres sur les barres (on saute l'en-tête i=0)
for i, y_coord in enumerate(pos_shifted):
    if i == 0: continue
    
    # Données et points de départ pour l'étiquetage
    vals = [terp_shifted[i], nrps_shifted[i], pks_shifted[i], ripp_shifted[i]]
    starts = [0, terp_shifted[i], terp_shifted[i]+nrps_shifted[i], terp_shifted[i]+nrps_shifted[i]+pks_shifted[i]]
    
    for val, start in zip(vals, starts):
        if val > 0:
            ax_chart.text(start + val/2, y_coord, f'{int(val)}', 
                         ha='center', va='center', weight='bold', fontsize=10, color='#333333')

# 5. Synchronisation des axes Y
ax_chart.set_ylim(0, len(df) + 1)
ax_chart.invert_yaxis()
ax_chart.axis('off')

# Mise à jour de la légende (4 colonnes)
ax_chart.legend(loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False, fontsize=12)

# --- SAUVEGARDE ---
plt.subplots_adjust(wspace=0.01)
plt.savefig("figure_phylogenie_bgc_v2_ripp.png", dpi=300, bbox_inches='tight')
plt.show()

print("\n[SUCCÈS] Le graphique a été mis à jour avec les fungal-RiPP.")
print(f"La couleur '{color_ripp}' a été appliquée.")