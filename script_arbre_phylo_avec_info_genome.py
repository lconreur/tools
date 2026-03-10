import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Bio import Phylo

# --- 1. CONFIGURATION VISUELLE ---
plt.rcParams['hatch.linewidth'] = 2.5
plt.rcParams['lines.linewidth'] = 2.0

# --- 2. CHARGEMENT DES DONNÉES ---
tree = Phylo.read("arbre_final.nwk", "newick")
leaf_names = [leaf.name for leaf in tree.get_terminals()]

df_raw = pd.read_excel('données pour arbre phylogénétique_clacla.xlsx')
# On filtre et on aligne l'Excel sur l'ordre des feuilles de l'arbre
df = df_raw[df_raw['Nom'].isin(leaf_names)].copy()
df = df.set_index('Nom').reindex(leaf_names).reset_index()

# Couleurs par Clade
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
    # DÉCALAGE DE 1.5 : Aligne le centre de la branche sur la 1ère ligne de données
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
# Ratios : [Arbre, Tableau (élargi), Histogramme]
fig, (ax_tree, ax_table, ax_chart) = plt.subplots(1, 3, figsize=(32, 22), 
                                                  gridspec_kw={'width_ratios': [0.5, 1.2, 1]})

# --- A. TRACÉ DE L'ARBRE (RECTANGULAIRE) ---
for clade in tree.find_clades():
    x_p, y_p = x_pos[clade], y_pos[clade]
    if not clade.is_terminal():
        child_ys = [y_pos[c] for c in clade]
        ax_tree.plot([x_p, x_p], [min(child_ys), max(child_ys)], color='black')
        for child in clade:
            ax_tree.plot([x_p, x_pos[child]], [y_pos[child], y_pos[child]], color='black')

# Prolongement des branches jusqu'au tableau
for leaf in tree.get_terminals():
    ax_tree.plot([x_pos[leaf], max_x], [y_pos[leaf], y_pos[leaf]], color='black')

ax_tree.set_ylim(0, len(df) + 1)
ax_tree.invert_yaxis()
ax_tree.axis('off')

# --- B. LE TABLEAU (AVEC COLONNE ORGANISME LARGE) ---
ax_table.axis('off')
df_display = df.copy()
df_display['Genome Assembly size (Mbp)'] = df_display['Genome Assembly size (Mbp)'].map('{:.2f}'.format)
df_display['Nombre de BGC par Mb'] = df_display['Nombre de BGC par Mb'].map('{:.2f}'.format)

the_table = ax_table.table(
    cellText=df_display[['Clade', 'Nom', 'Genome Assembly size (Mbp)', 'Nombre total de BGC', 'Nombre de BGC par Mb']].values, 
    colLabels=['Clade', 'Organisme', 'Taille (Mbp)', 'Total BGC', 'BGC / Mb'], 
    loc='center', 
    bbox=[0, 0, 1, 1] 
)

the_table.auto_set_font_size(False)
the_table.set_fontsize(11)

# RÉGLAGE LARGEUR COLONNES : si Clade (index 1) est à 0.45 (-> 45%)
col_widths = [0.18, 0.42, 0.13, 0.12, 0.15]

for (row, col), cell in the_table.get_celld().items():
    cell.set_width(col_widths[col])
    cell.set_height(1 / (len(df) + 1))

    # On force l'alignement horizontal au centre pour TOUTES les colonnes
    cell.set_text_props(ha='center', va='center')
    
    if row == 0:
        cell.set_facecolor('#333333')
        cell.set_text_props(weight='bold', color='white')
    else:
        clade_name = df.iloc[row-1]['Clade']
        color = clade_color_map[clade_name]
        if col == 1: # Organisme
            cell.get_text().set_style('italic')
            cell.get_text().set_color(color)
            cell.get_text().set_weight('bold')
        elif col == 0: # Clade
            cell.get_text().set_color(color)
            cell.get_text().set_weight('bold')
        if col in [0, 1]: cell.set_text_props(ha='center')

# --- C. L'HISTOGRAMME (DÉCALÉ À 1.5) ---
pos = np.arange(len(df)) + 0.5 
h_bars = 0.6
terp = df['Nombre de terpènes (sans les précursors)'].values
nrps = df['Nombre de NRPS et NRPS-like'].values
pks = df['Nombre de PKS (I et III)'].values

ax_chart.barh(pos, terp, h_bars, color='#B2E2E2', edgecolor='white', label='Terpènes')
ax_chart.barh(pos, nrps, h_bars, left=terp, color='#FFFFCC', hatch='/', edgecolor='#2CA25F', label='NRPS et NRPS-like')
ax_chart.barh(pos, pks, h_bars, left=terp+nrps, color='#FFB3B3', hatch='\\', edgecolor='#2B8CBE', label='PKS (Type I et III)')

# Chiffres sur les barres
for i, y_coord in enumerate(pos):
    for val, start in zip([terp[i], nrps[i], pks[i]], [0, terp[i], terp[i]+nrps[i]]):
        if val > 0:
            ax_chart.text(start + val/2, y_coord, f'{int(val)}', ha='center', va='center', weight='bold', fontsize=10)

ax_chart.set_ylim(ax_tree.get_ylim())
ax_chart.invert_yaxis()
ax_chart.axis('off')
ax_chart.legend(loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False)

# --- SAUVEGARDE ---
plt.subplots_adjust(wspace=0.01)
plt.savefig("figure_phylogenie_bgc_finale.png", dpi=300, bbox_inches='tight')
plt.show()