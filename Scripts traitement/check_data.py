import json
import csv
from pathlib import Path
from tqdm import tqdm

def find_missing_games(json_filename, csv_filename):
    # --- 1. Configuration des chemins ---
    script_dir = Path(__file__).resolve().parent
    json_path = script_dir / json_filename
    csv_path = script_dir / csv_filename
    output_path = script_dir / "missing_games.txt"

    # Vérification simple
    if not json_path.exists() or not csv_path.exists():
        print(f"Erreur : Impossible de trouver {json_filename} ou {csv_filename}")
        print(f"Dossier visé : {script_dir}")
        return

    # --- 2. Chargement des noms du JSON (Référence) ---
    print(f"Chargement du fichier JSON : {json_filename} ...")
    json_names = set()
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for game_info in data.values():
                if "name" in game_info:
                    # On stocke le nom tel quel
                    json_names.add(game_info["name"])
    except Exception as e:
        print(f"Erreur lors de la lecture du JSON : {e}")
        return

    print(f" -> {len(json_names)} jeux chargés depuis le JSON.")

    # --- 3. Vérification du CSV ---
    print(f"Analyse du fichier CSV : {csv_filename} ...")
    missing_games = set()
    processed_lines = 0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in tqdm(reader, desc="Comparaison", unit="ligne"):
                # Votre CSV a la forme : ID, "Nom du jeu", action, ...
                # Le nom est donc à l'index 1
                if len(row) > 1:
                    csv_game_name = row[1]
                    processed_lines += 1

                    # COMPARAISON STRICTE
                    if csv_game_name not in json_names:
                        test = False
                        #for json_name in json_names:
                        #    if (json_name != "") and ((csv_game_name in json_name) or (json_name in csv_game_name)):
                                #print("Jeu dans liste joueur: " + csv_game_name + "            " + "Nom jeu: " + json_name)
                        #        test = True
                        #        break
                        if not test:
                            missing_games.add(csv_game_name)
                        #if not test and row[2]=="play":
                        #    missing_games.remove(csv_game_name)

                        
    except Exception as e:
        print(f"Erreur lors de la lecture du CSV : {e}")
        return

    # --- 4. Rapport ---
    print("-" * 40)
    print(f"Lignes CSV traitées : {processed_lines}")
    print(f"Jeux du CSV introuvables dans le JSON : {len(missing_games)}")
    print("-" * 40)

    if missing_games:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Jeux manquants ({len(missing_games)}) :\n")
            f.write("===================================\n")
            for game in sorted(missing_games):
                f.write(f"{game}\n")
        print(f"La liste des jeux manquants a été écrite dans : {output_path.name}")
    else:
        print("Succès ! Tous les jeux du CSV sont présents dans le JSON.")

# --- Lancer le script ---
if __name__ == "__main__":
    # Remplacez par les noms exacts de vos fichiers
    json_file = 'games_cleaned.json' # Votre JSON propre
    csv_file = 'steam-200k_cleaned.csv'      # Votre CSV
    
    find_missing_games(json_file, csv_file)
