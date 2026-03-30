#FINAL
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. CONFIGURATION ET COULEURS ---
file_name = 'clade_org_bin_count_clacla.csv'

# Palette Tol Light + Sources (Optimisée Tritanopia)
bgc_color_map = {
    'NRPS':        '#FFEA80', # Jaune (Source A)
    'NRPS-like':   '#C99B61', # Ambre (Source B)
    'T1PKS':       '#9E2A2B', # Brique (Source A)
    'T3PKS':       "#C27AD4", #'#A06CD5', # Violet (Source B)
    'terpene':     '#88CCEE', # Bleu (Source unique)
    'fungal-RiPP': '#999933'  # Olive (Source unique)
}

# Couleurs fixes pour les Clades (ton image de référence)
clade_color_map_fixed = {
    'Residual Polyporoid': '#2E75B6',
    'Phlebioid': '#92D050',
    'Gelatoporia': '#833C0C',
    'Antrodia': '#A6A6A6',
    'Core Polyporoid': '#8CD3E8'
}

try:
    plt.close('all') # Nettoyage de la mémoire
    
    # Chargement des données
    df = pd.read_csv(file_name, sep=';')
    to_exclude = ['betalactone', 'indole', 'terpene-precursor']

    df_pivot = df.pivot_table(
        index=['Taxo_Clade', 'Genre_espece'], 
        columns='bin_label', 
        values='gbk_count', 
        aggfunc='sum'
    ).fillna(0)

    # Filtrage et Tri
    df_pivot = df_pivot.drop(columns=[c for c in to_exclude if c in df_pivot.columns])
    desired_order = ['terpene', 'NRPS', 'NRPS-like', 'T1PKS', 'T3PKS', 'fungal-RiPP']
    existing_columns = [c for c in desired_order if c in df_pivot.columns]
    df_pivot = df_pivot[existing_columns]
    df_pivot = df_pivot.sort_index(level=['Taxo_Clade', 'Genre_espece'])


    unique_clades = df_pivot.index.get_level_values('Taxo_Clade').unique()

    # --- 2. CONSTRUCTION DU DATAFRAME AVEC ESPACES (SPACERS) ---
    df_plot = pd.DataFrame()
    for i, clade in enumerate(unique_clades):
        clade_data = df_pivot.xs(clade, level='Taxo_Clade')
        df_plot = pd.concat([df_plot, clade_data])
        
        # Ajout d'une colonne vide (spacer) entre les clades
        if i < len(unique_clades) - 1:
            spacer_name = f" " * (i + 1) # Label unique pour l'axe X
            spacer = pd.DataFrame(0, index=[spacer_name], columns=df_pivot.columns)
            df_plot = pd.concat([df_plot, spacer])

    # --- 3. TRACÉ DU GRAPHIQUE CUMULÉ ---
    fig, ax = plt.subplots(figsize=(30, 15))

    df_plot.plot(
        kind='bar', 
        stacked=True, 
        ax=ax, 
        color=[bgc_color_map.get(c, '#7f7f7f') for c in df_plot.columns],
        width=0.85, 
        edgecolor='black', 
        linewidth=0.5
    )

    # --- 4. NAVIGATION ET STYLE (BOUCLE PAR CLADE) ---
    xticklabels = ax.get_xticklabels()
    current_idx = 0
    
    for i, clade in enumerate(unique_clades):
        clade_size = len(df_pivot.xs(clade, level='Taxo_Clade'))
        
        # Style des noms d'organismes (Italique + Couleur)
        color = clade_color_map_fixed.get(clade, '#000000') # Noir si non trouvé
        for j in range(current_idx, current_idx + clade_size):
            xticklabels[j].set_style('italic')
            xticklabels[j].set_color(color)
            xticklabels[j].set_weight('bold')
            xticklabels[j].set_fontsize(10)
        
        # Texte de la Clade sur DEUX LIGNES si nécessaire
        # On remplace l'espace par un saut de ligne
        display_clade = clade.replace(" ", "\n")
        
        center_pos = current_idx + (clade_size - 1) / 2
        ax.text(
            center_pos, 
            ax.get_ylim()[1] * 1.02, 
            display_clade, 
            ha='center', va='bottom', 
            color=color, 
            fontweight='bold', 
            fontsize=13,
            linespacing=0.9
        )

        # AJOUT DE LA LIGNE DE SÉPARATION (GRIS CLAIR)
        if i < len(unique_clades) - 1:
            separator_pos = current_idx + clade_size  # Milieu du spacer
            ax.axvline(x=separator_pos, color='#D3D3D3', linestyle='--', linewidth=1, zorder=0)

        # Avancement de l'index (Taille clade + 1 spacer)
        current_idx += (clade_size + 1)

    # --- 5. FINALISATION ET SAUVEGARDE ---
    plt.title('BGC global distribution', fontsize=26, pad=80)
    plt.ylabel('Number of BGC', fontsize=16)
    plt.xlabel('Organisms', fontsize=16)
    plt.xticks(rotation=45, ha='right')

    # Légende (Extérieure droite pour ne pas être coupée)
    legend_bgc = ax.legend(
        title='Types of BGC', 
        bbox_to_anchor=(1.02, 1), 
        loc='upper left', 
        frameon=False, 
        fontsize=13
    )

    plt.subplots_adjust(right=0.85, top=0.82, bottom=0.2)

    output_name = "analyse_bgc_CUMULE_final_pro.png"
    plt.savefig(
        output_name, 
        dpi=300, 
        bbox_extra_artists=(legend_bgc,), 
        bbox_inches='tight'
    )
    plt.show()

    print(f"\n[SUCCÈS] Le graphique a été généré : {output_name}")

except Exception as e:
    print(f"Erreur : {e}")