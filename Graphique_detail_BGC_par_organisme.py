# script complet et autonome pour générer les 5 figures
# === 1. Importer les librairies ===
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 2. Charger les fichiers ===
matrice = pd.read_csv("C:\\Users\\Laurence C\\Documents\\matrice_organisme_bin_label.csv", sep=",")
meta = pd.read_csv("C:\\Users\\Laurence C\\Documents\\organismes_metadata.csv", sep=",")

# === 3. Fusionner les métadonnées ===
df_merged = pd.merge(matrice, meta, on="organism", how="left")

# === 4. Définir et appliquer l'ordre des clades ===
ordre_clades = [
    "Core Polyporoid",
    "Antrodia",
    "Phlebioid",
    "Gelatoporia",
    "Residual Polyporoid"
]

df_merged["Taxo_Clade"] = pd.Categorical(df_merged["Taxo_Clade"], categories=ordre_clades, ordered=True)

# === 5. Trier par clade et espèce ===
df_merged = df_merged.sort_values(by=["Taxo_Clade", "Genre_espece"])
df_merged = df_merged.set_index(["Taxo_Clade", "Genre_espece"])

# === 6. Colonnes fonctionnelles à visualiser ===
colonnes_fonctionnelles = ['NRPS', 'PKS-NRP_Hybrids', 'PKSI', 'PKSother', 'other', 'terpene']

# === 7. Palette de couleurs pour les clades ===
df_heatmap = df_merged[colonnes_fonctionnelles]
clades = df_heatmap.index.get_level_values(0).to_list()
clade_uniques = list(df_heatmap.index.get_level_values(0).unique())
palette = sns.color_palette("Set2", len(clade_uniques))
clade_colors = dict(zip(clade_uniques, palette))

# === 8. Dictionnaire des figures à générer ===
figures = {
    "NRPS": "Fig3A",
    "PKS-NRP_Hybrids": "Fig3B",
    "PKSI": "Fig3C",
    "PKSother": "Fig3D",
    "other": "Fig3E",
    "terpene": "Fig3F"
}

# === 9. Boucle pour générer les figures ===
for metabolite, fig_label in figures.items():
    df_temp = df_merged.reset_index()[["Taxo_Clade", "Genre_espece", metabolite]]
    
    plt.figure(figsize=(14, 6))
    sns.barplot(
        data=df_temp,
        x="Genre_espece",
        y=metabolite,
        hue="Taxo_Clade",
        dodge=False,
        palette=clade_colors,
        edgecolor="black"
    )
    
    plt.xticks(rotation=90)
    plt.title(f"{fig_label} - Nombre de clusters de type {metabolite}", fontsize=16, pad=20)
    plt.ylabel("Nombre de clusters")
    plt.xlabel("Espèce")
    plt.legend(title="Clade", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Sauvegarde de l'image
    plt.savefig(f"{fig_label}_{metabolite}_clusters_par_espece.png", dpi=300)
    plt.show()