import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Bio import Phylo

# --- 1. CONFIGURATION ---
plt.rcParams['hatch.linewidth'] = 2.5
plt.rcParams['lines.linewidth'] = 2.0

# --- 2. CHARGEMENT ET ALIGNEMENT MANUEL ---
tree = Phylo.read("arbre_final.nwk", "newick")
leaf_names = [leaf.name for leaf in tree.get_terminals()]

df_raw = pd.read_excel('données pour arbre phylogénétique_clacla.xlsx')
df = df_raw[df_raw['Nom'].isin(leaf_names)].copy()
df = df.set_index('Nom').reindex(leaf_names).reset_index()

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

y_pos = {leaf: i + 0.5 for i, leaf in enumerate(tree.get_terminals())}

def fill_internal_y(clade):
    if clade.is_terminal(): return y_pos[clade]
    child_ys = [fill_internal_y(c) for c in clade]
    y_pos[clade] = sum(child_ys) / len(child_ys)
    return y_pos[clade]

x_pos = get_x_positions(tree)
fill_internal_y(tree.root)
max_x = max(x_pos.values())

# --- 4. FIGURE (6 PANNEAUX) ---
fig, (ax_tree, ax_names, ax_size, ax_total, ax_dens, ax_chart) = plt.subplots(1, 6, figsize=(38, 20), 
    gridspec_kw={'width_ratios': [0.5, 0.7, 0.25, 0.25, 0.25, 1.0]})

pos = np.arange(len(df)) + 0.5
h_bars = 0.6

# --- A. L'ARBRE ---
for clade in tree.find_clades():
    x_p, y_p = x_pos[clade], y_pos[clade]
    if not clade.is_terminal():
        child_ys = [y_pos[c] for c in clade]
        ax_tree.plot([x_p, x_p], [min(child_ys), max(child_ys)], color='black')
        for child in clade:
            ax_tree.plot([x_p, x_pos[child]], [y_pos[child], y_pos[child]], color='black')
for leaf in tree.get_terminals():
    ax_tree.plot([x_pos[leaf], max_x], [y_pos[leaf], y_pos[leaf]], color='black')

# --- B. LES NOMS ---
for i, row in df.iterrows():
    color = clade_color_map[row['Clade']]
    ax_names.text(0.5, i + 0.5, row['Nom'], va='center', ha='center', 
                  style='italic', weight='bold', color=color, fontsize=12)

# --- C. TAILLE GÉNOME ---
ax_size.barh(pos, df['Genome Assembly size (Mbp)'], h_bars, color='#E0E0E0', edgecolor='black')
for i, v in enumerate(df['Genome Assembly size (Mbp)']):
    ax_size.text(v + 0.5, i + 0.5, f'{v:.1f}', va='center', fontsize=10, weight='bold')

# --- D. TOTAL BGC ---
ax_total.barh(pos, df['Nombre total de BGC'], h_bars, color='#BBDEFB', edgecolor='black')
for i, v in enumerate(df['Nombre total de BGC']):
    ax_total.text(v + 0.5, i + 0.5, str(int(v)), va='center', fontsize=10, weight='bold')

# --- E. BGC / Mb ---
ax_dens.barh(pos, df['Nombre de BGC par Mb'], h_bars, color='#C8E6C9', edgecolor='black')
for i, v in enumerate(df['Nombre de BGC par Mb']):
    ax_dens.text(v + 0.02, i + 0.5, f'{v:.2f}', va='center', fontsize=10, weight='bold')

# --- F. HISTOGRAMME CUMULÉ ---
terp = df['Nombre de terpènes (sans les précursors)'].values
nrps = df['Nombre de NRPS et NRPS-like'].values
pks = df['Nombre de PKS (I et III)'].values

ax_chart.barh(pos, terp, h_bars, color='#B2E2E2', edgecolor='white', label='Terpènes')
ax_chart.barh(pos, nrps, h_bars, left=terp, color='#FFFFCC', hatch='/', edgecolor='#2CA25F', label='NRPS')
ax_chart.barh(pos, pks, h_bars, left=terp+nrps, color='#FFB3B3', hatch='\\', edgecolor='#2B8CBE', label='PKS')

for i, y_coord in enumerate(pos):
    for val, start in zip([terp[i], nrps[i], pks[i]], [0, terp[i], terp[i]+nrps[i]]):
        if val > 0:
            ax_chart.text(start + val/2, y_coord, f'{int(val)}', ha='center', va='center', weight='bold', fontsize=10)

# --- 5. SYNCHRONISATION ET MISE EN FORME ---
axes = [ax_tree, ax_names, ax_size, ax_total, ax_dens, ax_chart]
titles = ["", "Organisme", "Taille (Mbp)", "Total BGC", "BGC / Mb", "Détail BGC"]

for ax, title in zip(axes, titles):
    ax.set_ylim(0, len(df))
    ax.invert_yaxis()
    ax_tree.axis('off') # On garde l'axe de l'arbre caché
    ax.axis('off')
    if title:
        ax.set_title(title, weight='bold', size=14, pad=20)

ax_chart.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=False, fontsize=12)

plt.subplots_adjust(wspace=0.2)
plt.savefig("analyse_bioinfo_finale_valeurs.png", dpi=300, bbox_inches='tight')
plt.show()