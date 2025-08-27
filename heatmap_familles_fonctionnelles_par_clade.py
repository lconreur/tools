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

# 7bis. Générer des couleurs par Taxo_Clade
clades = df_heatmap.index.get_level_values(0).to_list()
clade_uniques = list(df_heatmap.index.get_level_values(0).unique())
palette = sns.color_palette("Set2", len(clade_uniques))
clade_colors = dict(zip(clade_uniques, palette))
row_colors = [clade_colors[clade] for clade in clades]

# 8. Afficher la heatmap avec clustermap sans clustering
g = sns.clustermap(
    df_heatmap,
    row_colors=row_colors,
    cmap="Blues",
    figsize=(16, 12),
    xticklabels=True,
    yticklabels=True,
    row_cluster=False,
    col_cluster=False
)

# 9. Ajouter une légende des couleurs
for label in clade_uniques:
    g.ax_col_dendrogram.bar(0, 0, color=clade_colors[label], label=label, linewidth=0)
g.ax_col_dendrogram.legend(loc="center", ncol=3)

# 10. Sauvegarder et afficher
plt.title("Heatmap des familles fonctionnelles par clade et espèce", pad=80)
plt.savefig("heatmap_fonctionnelle_par_clade_colorée.png", dpi=300)
plt.show()