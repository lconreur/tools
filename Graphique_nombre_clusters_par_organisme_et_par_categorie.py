import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Charger les fichiers ===
matrice = pd.read_csv("C:\\Users\\Laurence C\\Documents\\matrice_organisme_bin_label.csv", sep=",")
meta = pd.read_csv("C:\\Users\\Laurence C\\Documents\\organismes_metadata.csv", sep=",")

# === 2. Fusionner les métadonnées ===
df_merged = pd.merge(matrice, meta, on="organism", how="left")

# === 3. Définir l’ordre des clades ===
ordre_clades = [
    "Core Polyporoid",
    "Antrodia",
    "Phlebioid",
    "Gelatoporia",
    "Residual Polyporoid"
]
df_merged["Taxo_Clade"] = pd.Categorical(df_merged["Taxo_Clade"], categories=ordre_clades, ordered=True)

# === 4. Colonnes d’intérêt ===
colonnes_clusters = ['NRPS', 'PKS-NRP_Hybrids', 'PKSI', 'PKSother', 'other', 'terpene']

# === 5. Calculer la moyenne par espèce ===
df_moy = df_merged.groupby(["Taxo_Clade", "Genre_espece"])[colonnes_clusters].mean().reset_index()

# === 6. Trier selon Clade puis espèce ===
df_moy = df_moy.sort_values(by=["Taxo_Clade", "Genre_espece"])

# === 7. Préparer le DataFrame pour le barplot empilé ===
df_moy.set_index("Genre_espece", inplace=True)

# === 8. Palette pastel pour les catégories ===
palette = sns.color_palette("pastel", n_colors=len(colonnes_clusters))
palette_dict = dict(zip(colonnes_clusters, palette))

# === 9. Plot empilé ===
plt.figure(figsize=(16, 8))
bottoms = pd.Series([0] * len(df_moy), index=df_moy.index)

for cat in colonnes_clusters:
    plt.bar(
        df_moy.index,
        df_moy[cat],
        bottom=bottoms,
        label=cat,
        color=palette_dict[cat],
        edgecolor='black'
    )
    bottoms += df_moy[cat]

# === 10. Mise en forme ===
plt.xticks(rotation=90)
plt.ylabel("Nombre moyen de clusters")
plt.xlabel("Espèces")
plt.title("Répartition moyenne des types de clusters par espèce")
plt.legend(title="Type de cluster", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# === 11. Export (optionnel) ===
plt.savefig("barplot_clusters_par_espece_ordre_clade.png", dpi=300)

plt.show()
