import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Charger fichier ===
matrice = pd.read_csv("C:\\Users\\Laurence C\\Documents\\ton_fichier1.csv", sep=";")

# === Ajouter colonne famille ===
matrice["famille"] = matrice["id"].apply(lambda x: f"FAM_{int(x):03}")

def pareto_analysis(df, bin_label, seuil=0.8):
    df_bin = df[df["bin_label"] == bin_label]
    counts = df_bin.groupby("famille")["id"].count().sort_values(ascending=False)
    cumul = counts.cumsum() / counts.sum()
    nb_familles = (cumul <= seuil).sum() + 1
    return counts, cumul, nb_familles

bin_labels = matrice["bin_label"].unique()
plt.figure(figsize=(14, 8))
colors = sns.color_palette("tab10", len(bin_labels))

for i, cat in enumerate(bin_labels):
    counts, cumul, nb_familles = pareto_analysis(matrice, cat)
    x_vals = range(1, len(cumul) + 1)
    y_vals = cumul.values
    plt.plot(x_vals, y_vals, label=cat, color=colors[i])
    
    # Valeur y où s'arrête le trait vertical
    y_trait = y_vals[nb_familles - 1]
    
    # Tracé du trait vertical limité à y_trait
    plt.vlines(nb_familles, 0, y_trait, color=colors[i], linestyle="--", alpha=0.7)
    
    # Annotation du nombre de familles sous l'axe des x
    plt.text(
        nb_familles, -0.05,  # un peu sous 0 pour éviter overlap
        f"{nb_familles}",
        color=colors[i],
        rotation=90,
        verticalalignment='top',
        horizontalalignment='center',
        fontsize=10,
        fontweight='bold'
    )

plt.axhline(0.8, color="red", linestyle="--", label="Seuil 80%")

plt.xlabel("Nombre de familles (triées par fréquence)")
plt.ylabel("Proportion cumulative des clusters")
plt.title("Courbes de Pareto des familles par catégorie de métabolites secondaires")
plt.legend(title="Catégorie")
# plt.ylim(-0.1, 1.05)
plt.grid(True)
plt.tight_layout()
plt.show()
