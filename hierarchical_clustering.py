import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. Chargement et Pivot
file_name = 'clade_org_bin_count_clacla.csv'
df = pd.read_csv(file_name, sep=';')
df_pivot = df.pivot_table(
    index=['Taxo_Clade', 'Genre_espece'], 
    columns='bin_label', 
    values='gbk_count', 
    aggfunc='sum'
).fillna(0)

# 2. Couleurs (Cohérence Graph 1)
unique_clades = df_pivot.index.get_level_values('Taxo_Clade').unique()
clade_colors_palette = plt.get_cmap('tab20', len(unique_clades))
clade_color_map = {clade: clade_colors_palette(i) for i, clade in enumerate(unique_clades)}
row_colors = [clade_color_map[clade] for clade in df_pivot.index.get_level_values('Taxo_Clade')]

# 3. Création de la Clustermap
g = sns.clustermap(
    df_pivot,
    row_cluster=True,      
    col_cluster=False,     
    row_colors=row_colors, 
    cmap="Blues",
    figsize=(20, 14), # Légèrement plus grand pour le confort visuel
    xticklabels=True,
    yticklabels=True,
    dendrogram_ratio=(0.12, 0.05),
    cbar_pos=None # On gérera la cbar manuellement ou on la laisse par défaut
)

# 4. Labels Y en italique et en couleur
reordered_indices = g.dendrogram_row.reordered_ind
yticklabels = g.ax_heatmap.get_yticklabels()

for i, idx_original in enumerate(reordered_indices):
    clade = df_pivot.index[idx_original][0]
    espece = df_pivot.index[idx_original][1]
    yticklabels[i].set_text(espece)
    yticklabels[i].set_color(clade_color_map[clade])
    yticklabels[i].set_style('italic')
    yticklabels[i].set_weight('bold')

g.ax_heatmap.set_yticklabels(yticklabels)

# 5. NOUVELLE LÉGENDE HORIZONTALE SOUS LE TITRE
clade_patches = [mpatches.Patch(color=clade_color_map[c], label=c) for c in unique_clades]

# On crée la légende sur la figure entière (g.fig) plutôt que sur un axe
leg = g.fig.legend(
    handles=clade_patches,
    title='Taxo_Clade',
    loc='upper center', 
    bbox_to_anchor=(0.5, 0.94), # Position juste sous le titre
    ncol=min(len(unique_clades), 5), # Nombre de colonnes (ajustable selon le nombre de clades)
    fontsize=11,
    title_fontsize=13,
    frameon=False
)

# 6. Finalisation et Marges
g.fig.suptitle('Classification des organismes par profil de BGC', fontsize=22, y=0.98)
g.ax_heatmap.set_xlabel("Familles de BGC", fontsize=14)
g.ax_heatmap.set_ylabel("Espèces", fontsize=14)

# On réajuste les marges pour laisser de la place au titre + légende en haut
plt.subplots_adjust(top=0.85, bottom=0.1, left=0.1, right=0.95)

plt.savefig("graph2_clustermap_legende_top.png", dpi=300, bbox_inches='tight')
plt.show()