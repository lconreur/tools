import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Chargement fichiers
df_familles = pd.read_csv(r"C:\Users\Laurence C\Documents\ton_fichier1.csv", sep=";")
df_meta = pd.read_csv(r"C:\Users\Laurence C\Documents\organismes_metadata.csv", sep=",")

# Fusionner pour récupérer les infos taxo et les ids des familles
df = pd.merge(df_familles, df_meta, on='organism', how='left')

# Créer une colonne 'famille_label' avec les id formatés, ex: id_x=1 => FAM_001
df['famille_label'] = df['id_x'].apply(lambda x: f"FAM_{int(x):03d}")

# Grouper par Taxo_Clade, famille_label, bin_label, compter organismes uniques
df_count = df.groupby(['Taxo_Clade', 'famille_label', 'bin_label']).size().reset_index(name='count')

# Trier les familles par bin_label puis famille_label
df_count = df_count.sort_values(by=['bin_label', 'famille_label'])

# Liste des familles triées
familles_ordonnee = df_count.drop_duplicates(subset='famille_label')['famille_label'].tolist()

# Pivot pour matrice 2D (Taxo_Clade en ligne, familles en colonne)
matrice = df_count.pivot(index='Taxo_Clade', columns='famille_label', values='count').fillna(0)

# Extraire bin_label correspondant aux familles ordonnées
bin_labels_ordonnees = df_count.drop_duplicates('famille_label').set_index('famille_label').loc[familles_ordonnee, 'bin_label']

# Créer une palette de couleurs distinctes pour chaque bin_label
palette = sns.color_palette("tab10", n_colors=bin_labels_ordonnees.nunique())
color_mapping = dict(zip(bin_labels_ordonnees.unique(), palette))

# Assigner une couleur à chaque famille selon son bin_label
colors = bin_labels_ordonnees.map(color_mapping)

# Plot heatmap
plt.figure(figsize=(40, 6))  # plus large (24 au lieu de 16)
ax = sns.heatmap(matrice[familles_ordonnee], cmap="Blues", linewidths=0.5, linecolor='gray')

plt.title("Répartition des familles (FAM_xxx) par Taxo_Clade")
plt.xlabel("Familles")
plt.ylabel("Taxo_Clade")

# Modifier les étiquettes de l'axe x : uniquement FAM_xxx, rotation et couleur individuellement
xticks = ax.get_xticklabels()
for tick, color in zip(xticks, colors):
    tick.set_color(color)
    tick.set_rotation(90)
    tick.set_ha('center')
    tick.set_fontsize(15)  # police plus petite (par exemple 8)

# Ajouter une légende pour les bin_label
from matplotlib.patches import Patch
legend_handles = [Patch(color=color_mapping[bin_label], label=bin_label) for bin_label in color_mapping]

plt.legend(handles=legend_handles, title='bin_label',
           loc='upper center', bbox_to_anchor=(0.5, -0.35), ncol=6)

plt.tight_layout()
plt.show()
