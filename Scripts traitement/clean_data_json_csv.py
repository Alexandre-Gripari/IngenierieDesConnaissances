import csv
import json
import re
from pathlib import Path

# --- 1. CONFIGURATION GLOBALE (REGEX & CONSTANTES) ---

# A. Configuration pour les chiffres romains
roman_map = {
    "I": "1", "II": "2", "III": "3", "IV": "4", "V": "5",
    "VI": "6", "VII": "7", "VIII": "8", "IX": "9", "X": "10",
    "XI": "11", "XII": "12", "XIII": "13", "XIV": "14", "XV": "15",
    "XVI": "16", "XVII": "17", "XVIII": "18", "XIX": "19", "XX": "20",
    "XXI": "21", "XXII": "22", "XXIII": "23", "XXIV": "24", "XXV": "25",
    "XXX": "30", "XL": "40", "L": "50"
}

PATTERN_HYPHEN = re.compile(r" -.*")

# Création du regex pour les chiffres romains (compilé une seule fois pour la performance)
roman_pattern_str = r'\b(' + '|'.join(sorted(roman_map.keys(), key=len, reverse=True)) + r')\b'
PATTERN_ROMAN = re.compile(roman_pattern_str)

def replace_roman(match):
    """Fonction helper pour le remplacement regex"""
    return roman_map[match.group(0)]


# --- 2. LA FONCTION DE NETTOYAGE UNIQUE ---
def normalize_game_name(name, json=True):
    """
    Cette fonction prend un nom brut et retourne le nom nettoyé.
    Elle est utilisée par le CSV et le JSON.
    """
    global PATTERN_HYPHEN
    if not name or not isinstance(name, str):
        return name

    current_name = name


    if json:
        PATTERN_HYPHEN = re.compile(r"")
    # 1. Suppression du suffixe avec tiret (Ex: "Civ V - Addon" -> "Civ V")
    current_name = re.sub(PATTERN_HYPHEN, "", current_name)
    current_name = current_name.strip()

    # 2. Corrections spécifiques (Hardcoded)
    if "Assassins Creed Unity" == current_name:
        current_name = "Assassin's Creed Unity"
    if "Assassins Creed Chronicles China" == current_name:
        current_name = "Assassin’s Creed Chronicles China"

    # 3. Nettoyage des caractères spéciaux
    replacements = {
        ':': '', '!': '', '²': '', '™': '', '®': '',
        '’': '\''  # Uniformisation des apostrophes
    }
    for char, replacement in replacements.items():
        if char in current_name:
            current_name = current_name.replace(char, replacement)

    # 4. Conversion des chiffres romains (Ex: "Civ V" -> "Civ 5")
    current_name = PATTERN_ROMAN.sub(replace_roman, current_name)

    # 5. Minuscules et strip final
    return current_name.lower()


# --- 3. TRAITEMENT DU CSV ---
def process_csv_file(input_filename, output_filename):
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / input_filename
    output_path = script_dir / output_filename

    if not input_path.exists():
        print(f"❌ (CSV) Erreur : Fichier '{input_filename}' introuvable.")
        return

    print(f"🔄 Traitement CSV : {input_filename}...")
    count_modified = 0

    with open(input_path, 'r', encoding='utf-8') as f_in, \
            open(output_path, 'w', encoding='utf-8', newline='') as f_out:

        reader = csv.reader(f_in)
        writer = csv.writer(f_out)

        for row in reader:
            if len(row) > 1:  # On suppose que le nom est à l'index 1
                original_name = row[1]

                # APPEL DE LA FONCTION DE NETTOYAGE
                clean_name = normalize_game_name(original_name, False)

                if clean_name != original_name:  # Comparaison approximative
                    row[1] = clean_name
                    count_modified += 1

            writer.writerow(row)

    print(f"✅ (CSV) Terminé ! {count_modified} lignes modifiées. Sauvegardé dans {output_filename}")


# --- 4. TRAITEMENT DU JSON ---
def process_json_file(input_filename, output_filename):
    PATTERN_HYPHEN = re.compile(r"")
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / input_filename
    output_path = script_dir / output_filename

    if not input_path.exists():
        print(f"❌ (JSON) Erreur : Fichier '{input_filename}' introuvable.")
        return

    print(f"🔄 Traitement JSON : {input_filename}...")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Erreur : Le fichier n'est pas un JSON valide.")
        return

    count_modified = 0

    # Itération sur le dictionnaire JSON
    for game_id, game_info in data.items():
        if "name" in game_info:
            original_name = game_info["name"]

            # APPEL DE LA FONCTION DE NETTOYAGE
            clean_name = normalize_game_name(original_name)

            if clean_name != original_name:  # Si changement
                game_info["name"] = clean_name
                count_modified += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ (JSON) Terminé ! {count_modified} jeux modifiés. Sauvegardé dans {output_filename}")


# --- 5. EXÉCUTION PRINCIPALE ---
if __name__ == "__main__":
    print("🚀 Démarrage du nettoyage global...\n")

    # 1. Lancer le nettoyage CSV
    process_csv_file('steam-200k.csv', 'steam-200k_cleaned.csv')

    print("-" * 30)

    # 2. Lancer le nettoyage JSON
    process_json_file('games.json', 'games_cleaned.json')

    print("\n🏁 Tout est terminé.")