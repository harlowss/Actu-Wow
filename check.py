import os, json, re, requests

URL = "https://worldofwarcraft.blizzard.com/fr-fr/news"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
FICHIER = "seen.json"

html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
liens = []
for chemin, id_ in re.findall(r'href="(/fr-fr/news/(\d+)/[^"]+)"', html):
    if id_ not in [i for i, _ in liens]:
        liens.append((id_, chemin))

premier_lancement = not os.path.exists(FICHIER)
vus = [] if premier_lancement else json.load(open(FICHIER))

for id_, chemin in reversed(liens):
    if id_ not in vus:
        if not premier_lancement:
            requests.post(WEBHOOK, json={"content": f"📰 Nouvelle actu WoW : https://worldofwarcraft.blizzard.com{chemin}"})
        vus.append(id_)

json.dump(vus[-200:], open(FICHIER, "w"))
