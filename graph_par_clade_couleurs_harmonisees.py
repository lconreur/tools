import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. Chargement et préparation des données
file_name = 'clade_org_bin_count_clacla.csv'

try:
    df = pd.read_csv(file_name, sep=';')

    # EXCLUSION identique au graph cumulé
    to_exclude = ['betalactone', 'indole', 'terpene-precursor']

    df_pivot = df.pivot_table(
        index=['Taxo_Clade', 'Genre_espece'], 
        columns='bin_label', 
        values='gbk_count', 
        aggfunc='sum'
    ).fillna(0)

    # Filtrage des colonnes exclues
    df_pivot = df_pivot.drop(columns=[c for c in to_exclude if c in df_pivot.columns])
    df_pivot = df_pivot.sort_index(level=['Taxo_Clade', 'Genre_espece'])

    # 2. TES COULEURS EXACTES
    bgc_color_map = {
        'NRPS': '#AEC7E8',       # Bleu ciel poudré
        'NRPS-like': '#D1E3F3',  # Bleu très pâle
        'T1PKS': '#FFADAD',      # Saumon / Rose pastel
        'T3PKS': '#FFD6A5',      # Pêche / Crème
        'terpene': "#C5C5B8",    # Jaune paille pastel (ton gris beige)
        'fungal-RiPP': '#CAFFBF' # Menthe très douce
    }

    # 3. Couleurs des Clades (tab20)
    unique_clades = df_pivot.index.get_level_values('Taxo_Clade').unique()
    clade_colors = plt.get_cmap('tab20', len(unique_clades))
    clade_color_map = {clade: clade_colors(i) for i, clade in enumerate(unique_clades)}

    # 4. Boucle pour générer un graphique par type de BGC restant
    unique_bgcs = df_pivot.columns.tolist()

    for bgc_type in unique_bgcs:
        fig, ax = plt.subplots(figsize=(24, 12))
        
        data_to_plot = df_pivot[bgc_type]
        current_color = bgc_color_map.get(bgc_type, '#7f7f7f')

        data_to_plot.plot(
            kind='bar', 
            ax=ax,
            color=current_color,
            width=0.8, 
            edgecolor='black', 
            linewidth=0.5
        )

        # 5. Axe X (Espèces)
        species_labels = [index[1] for index in df_pivot.index]
        ax.set_xticklabels(species_labels)

        xticklabels = ax.get_xticklabels()
        for i, label in enumerate(xticklabels):
            clade_name = df_pivot.index[i][0]
            label.set_style('italic')
            label.set_color(clade_color_map[clade_name])
            label.set_weight('bold')
            label.set_fontsize(10)

        # 6. Délimitation des Clades
        current_pos = -0.5
        for clade in unique_clades:
            count = (df_pivot.index.get_level_values('Taxo_Clade') == clade).sum()
            ax.axvspan(current_pos, current_pos + count, color=clade_color_map[clade], alpha=0.1)
            
            plt.text(
                current_pos + count/2, 
                ax.get_ylim()[1] * 1.02, 
                clade, 
                ha='center', va='bottom', 
                color=clade_color_map[clade], 
                fontweight='bold',
                fontsize=12
            )
            current_pos += count

        # 7. Légendes
        bgc_patch = mpatches.Patch(color=current_color, label=bgc_type)
        legend_bgc = ax.legend(handles=[bgc_patch], title='Type de BGC', bbox_to_anchor=(1.02, 1), loc='upper left')
        ax.add_artist(legend_bgc)

        clade_patches = [mpatches.Patch(color=clade_color_map[c], label=c) for c in unique_clades]
        plt.legend(handles=clade_patches, title='Clades', bbox_to_anchor=(1.02, 0.45), loc='upper left')

        # 8. Finalisation
        plt.title(f'Distribution des BGC : {bgc_type}', fontsize=22, pad=50)
        plt.ylabel('Nombre de gbk', fontsize=14)
        plt.xlabel('Organismes', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(right=0.82, top=0.88, bottom=0.22)

        # Sauvegarde
        safe_name = bgc_type.replace('/', '_').replace(' ', '_')
        output_filename = f"analyse_bgc_{safe_name}.png"
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        plt.close(fig) 
        
        print(f"Graphique généré : {output_filename}")

except Exception as e:
    print(f"Erreur : {e}")