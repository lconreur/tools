#FINAL
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from Bio import Phylo

# --- 1. CONFIGURATION VISUELLE ET COULEURS ---
plt.rcParams['lines.linewidth'] = 1.5

# Dictionnaire de couleurs fixe pour les Clades
clade_color_map = {
    'Residual Polyporoid': '#2E75B6',
    'Phlebioid': '#92D050',
    'Gelatoporia': '#833C0C',
    'Antrodia': '#A6A6A6',
    'Core Polyporoid': '#8CD3E8'
}

# --- 2. CHARGEMENT DES DONNÉES ---
tree = Phylo.read("arbre_final.nwk", "newick")
leaf_names = [leaf.name for leaf in tree.get_terminals()]

file_name = 'données pour arbre phylogénétique_clacla_2.xlsx' 
try:
    df_raw = pd.read_excel(file_name)
except FileNotFoundError:
    print(f"Erreur : Le fichier '{file_name}' est introuvable.")
    exit()

df = df_raw[df_raw['Nom'].isin(leaf_names)].copy()
df = df.set_index('Nom').reindex(leaf_names).reset_index()

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

# --- B. LE TABLEAU ---
ax_table.axis('off')
df_display = df.copy()
df_display['Genome Assembly size (Mbp)'] = df_display['Genome Assembly size (Mbp)'].map('{:.2f}'.format)
col_total_bgc = 'Nombre total de BGC sans tprec, indole et betalactone)'
if col_total_bgc not in df_display.columns: col_total_bgc = 'Nombre total de BGC'
df_display['Nombre de BGC par Mb'] = df_display['Nombre de BGC par Mb'].map('{:.2f}'.format)

table_data = df_display[['Clade', 'Nom', 'Genome Assembly size (Mbp)', col_total_bgc, 'Nombre de BGC par Mb']].values
table_labels = ['Clade', 'Organism', 'Size (Mbp)', 'Total BGC', 'BGC / Mb']

the_table = ax_table.table(cellText=table_data, colLabels=table_labels, loc='center', bbox=[0, 0, 1, 1], cellLoc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(11)

col_widths = [0.18, 0.42, 0.14, 0.13, 0.13]
for (row, col), cell in the_table.get_celld().items():
    cell.set_width(col_widths[col])
    cell.set_height(1 / (len(df) + 1))
    cell.set_edgecolor('#D3D3D3')
    if row == 0:
        cell.set_facecolor('#4F4F4F')
        cell.get_text().set_color('white')
        cell.get_text().set_weight('bold')
    else:
        clade_name = df.iloc[row-1]['Clade']
        color = clade_color_map.get(clade_name, '#000000')
        if col == 0: cell.get_text().set_color(color); cell.get_text().set_weight('bold')
        elif col == 1: cell.get_text().set_color(color); cell.get_text().set_weight('bold'); cell.get_text().set_style('italic')
        else: cell.get_text().set_color('black')

# --- C. L'HISTOGRAMME (PALETTE TOL LIGHT + SOURCES) ---
terp = df['Nombre de terpènes (sans les précursors)'].values
nrps = df['Nombre de NRPS et NRPS-like'].values
pks  = df['Nombre de PKS (I et III)'].values
ripp = df['Nombre de fungal-RiPP'].values

# Couleurs Tol Light : Terpènes (Bleu), NRPS (Sable), PKS (Rose), RiPP (Olive)
c_terp, c_nrps, c_pks, c_ripp = "#88CCEE", "#DDCC77", "#CC6677", "#999933"

terp_s = np.insert(terp, 0, 0); nrps_s = np.insert(nrps, 0, 0)
pks_s = np.insert(pks, 0, 0); ripp_s = np.insert(ripp, 0, 0)
pos_s = np.arange(len(df) + 1) + 0.5

ax_chart.barh(pos_s, terp_s, 0.6, color=c_terp, edgecolor='black', linewidth=0.5, label='Terpenes')
ax_chart.barh(pos_s, nrps_s, 0.6, left=terp_s, color=c_nrps, edgecolor='black', linewidth=0.5, label='NRPS + like')
ax_chart.barh(pos_s, pks_s, 0.6, left=terp_s+nrps_s, color=c_pks, edgecolor='black', linewidth=0.5, label='PKS (I & III)')
ax_chart.barh(pos_s, ripp_s, 0.6, left=terp_s+nrps_s+pks_s, color=c_ripp, edgecolor='black', linewidth=0.5, label='fungal-RiPP')

for i, y_coord in enumerate(pos_s):
    if i == 0: continue
    vals = [terp_s[i], nrps_s[i], pks_s[i], ripp_s[i]]
    starts = [0, terp_s[i], terp_s[i]+nrps_s[i], terp_s[i]+nrps_s[i]+pks_s[i]]
    for val, start in zip(vals, starts):
        if val > 0:
            ax_chart.text(start + val/2, y_coord, f'{int(val)}', ha='center', va='center', weight='bold', fontsize=10, color='#333333')

ax_chart.set_ylim(0, len(df) + 1); ax_chart.invert_yaxis(); ax_chart.axis('off')

# --- 7. LÉGENDES (SANS CLADES, SANS COUPURES) ---
# La légende est placée à droite (1.05) pour ne pas être DANS le graphique
legend_bgc = ax_chart.legend(title='Types of BGC', 
                             bbox_to_anchor=(0.95, 1), 
                             loc='upper left', 
                             frameon=False, 
                             fontsize=12)

# --- 8. FINALISATION ET SAUVEGARDE ---
plt.subplots_adjust(wspace=0.01)

# L'astuce bbox_extra_artists empêche la légende d'être coupée à l'export
plt.savefig("figure_phylogenie_bgc_final.png", 
            dpi=300, 
            bbox_extra_artists=(legend_bgc,), 
            bbox_inches='tight')

plt.show()

print("\n[SUCCÈS] Graphique généré avec Tol Light. Légende Clade supprimée. Exportation complète.")