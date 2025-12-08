import pandas as pd
import os

# Noms des fichiers (doivent être dans le même dossier que ce script)
csv_file = 'steam-200k_cleaned.csv'
txt_file = 'missing_games.txt'
output_file = 'steam-200k_filtered.csv'


def clean_steam_data():
    # 1. Vérification de la présence des fichiers
    if not os.path.exists(csv_file) or not os.path.exists(txt_file):
        print("Erreur : Assurez-vous que 'steam-200k_cleaned.csv' et 'missing_game.txt' sont bien dans le dossier.")
        return

    print("Chargement de la liste des jeux à supprimer...")

    # 2. Lecture du fichier txt et création d'un "set" (ensemble) pour une recherche rapide
    # On utilise .strip() pour enlever les retours à la ligne et les espaces invisibles
    with open(txt_file, 'r', encoding='utf-8') as f:
        # On met tout en set pour que la suppression soit instantanée
        missing_games = set(line.strip() for line in f if line.strip())

    print(f"{len(missing_games)} jeux identifiés à supprimer.")

    print("Chargement du fichier CSV...")
    # 3. Lecture du CSV
    # On définit les noms de colonnes car le fichier d'origine n'a souvent pas d'en-tête
    # Colonnes typiques : User ID, Game Name, Behavior, Value, 0
    df = pd.read_csv(csv_file, header=None, names=['user_id', 'game_name', 'behavior', 'value'])

    initial_count = len(df)
    print(f"Lignes totales avant nettoyage : {initial_count}")

    # 4. Filtrage
    # On garde (~) les lignes où le 'game_name' N'EST PAS (.isin) dans 'missing_games'
    # Note : Cela suppose que les noms sont écrits exactement de la même façon (minuscules/majuscules)
    df_cleaned = df[~df['game_name'].isin(missing_games)]

    final_count = len(df_cleaned)
    removed_count = initial_count - final_count

    print(f"Lignes supprimées : {removed_count}")
    print(f"Lignes restantes : {final_count}")

    # 5. Sauvegarde du nouveau fichier
    # index=False pour ne pas ajouter une colonne de numérotation
    # header=False pour garder le format original sans en-tête
    df_cleaned.to_csv(output_file, index=False, header=True)

    print(f"Terminé ! Le fichier nettoyé a été sauvegardé sous : {output_file}")


if __name__ == "__main__":
    clean_steam_data()