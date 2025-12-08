import pandas as pd
import json

folder = './Données'
csv_name = 'steam-200k.csv'
csv_file = folder + '/' + csv_name
json_name = 'games.json'
json_file = folder + '/' + json_name

df = pd.read_csv(csv_file)

target_games = set(df['game_name'].unique())

print(f"Nombre de jeux uniques trouvés dans le CSV : {len(target_games)}")

with open(json_file, 'r', encoding='utf-8') as f:
    all_games = json.load(f)

filtered_games = {}

for app_id, game_data in all_games.items():
    game_name_json = game_data.get('name')
    
    if game_name_json in target_games:
        filtered_games[app_id] = game_data

with open(json_name, 'w', encoding='utf-8') as f:
    json.dump(filtered_games, f, indent=4)

print(f"Filtrage terminé. {len(filtered_games)} jeux conservés.")
print(f"Le résultat a été sauvegardé dans '{json_name}'")
