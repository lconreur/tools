#vdef 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Charger les fichiers
matrice = pd.read_csv("C:\\Users\\Laurence C\\Documents\\matrice_organisme_bin_label.csv", sep=",")
meta = pd.read_csv("C:\\Users\\Laurence C\\Documents\\organismes_metadata.csv", sep=",")

# 2. Fusionner avec les métadonnées (sur 'organism')
df_merged = pd.merge(matrice, meta, on="organism", how="left")

# 3. Définir l'ordre personnalisé des clades
ordre_clades = [
    "Core Polyporoid",
    "Antrodia",
    "Phlebioid",
    "Gelatoporia",
    "Residual Polyporoid"
]

# 4. Convertir en catégorie ordonnée
df_merged["Taxo_Clade"] = pd.Categorical(df_merged["Taxo_Clade"], categories=ordre_clades, ordered=True)

# 5. Trier par clade puis par espèce
df_merged = df_merged.sort_values(by=["Taxo_Clade", "Genre_espece"])

# 6. Définir un index multi-niveau
df_merged = df_merged.set_index(["Taxo_Clade", "Genre_espece"])

# 7. Garder uniquement les colonnes fonctionnelles
colonnes_fonctionnelles = ['NRPS', 'PKS-NRP_Hybrids', 'PKSI', 'PKSother', 'other', 'terpene']
df_heatmap = df_merged[colonnes_fonctionnelles]


# 7bis. Renommer les colonnes pour plus de compacité (retours à la ligne)
rename_cols = {
    'NRPS': 'NRPS',
    'PKS-NRP_Hybrids': 'PKS-\nNRP_Hybrids',
    'PKSI': 'PKSI',
    'PKSother': 'PKS\nother',
    'other': 'Other',
    'terpene': 'Terpene'
}
df_heatmap = df_merged[colonnes_fonctionnelles].rename(columns=rename_cols)

# 7ter. Générer des couleurs par Taxo_Clade
clades = df_heatmap.index.get_level_values(0).to_list()
clade_uniques = list(df_heatmap.index.get_level_values(0).unique())
palette = sns.color_palette("Set2", len(clade_uniques))
clade_colors = dict(zip(clade_uniques, palette))
row_colors = [clade_colors[clade] for clade in clades]

# 8. Extraire les labels à afficher : uniquement Genre_espece
y_labels = df_heatmap.index.get_level_values("Genre_espece")

# 9. Afficher la heatmap avec clustermap (sans clustering)
g = sns.clustermap(
    df_heatmap,
    row_colors=row_colors,
    cmap="Blues",
    figsize=(13, 12),
    xticklabels=True,
    yticklabels=y_labels,
    row_cluster=False,
    col_cluster=False,
    cbar_pos=(0.1, 0.4, 0.03, 0.4),
    )

# 10. Appliquer les couleurs aux labels Y selon le clade
for tick_label, clade in zip(g.ax_heatmap.get_yticklabels(), clades):
    tick_label.set_color(clade_colors[clade])

# 11. Ajouter une légende des couleurs
for label in clade_uniques:
    g.ax_col_dendrogram.bar(0, 0, color=clade_colors[label], label=label, linewidth=0)
g.ax_col_dendrogram.legend(loc="center", ncol=3)

# 12. Sauvegarder et afficher
plt.title("Heatmap \ndes familles fonctionnelles \npar clade et espèce", pad=80)
plt.savefig("heatmap_fonctionnelle_par_clade_colorée_labels_colores.png", dpi=300)
plt.show()
