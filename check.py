import os, json, re, requests

URLS = [
    "https://news.blizzard.com/fr-fr/feed/world-of-warcraft",
    "https://news.blizzard.com/fr-fr/world-of-warcraft",
]
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
FICHIER = "seen.json"

liens = []
for url in URLS:
    texte = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
    for chemin in re.findall(r'(?:https://news\.blizzard\.com)?(/fr-fr/[a-z0-9\-/]*?/\d{5,}/[a-z0-9\-]+)', texte):
        lien = "https://news.blizzard.com" + chemin
        if lien not in liens:
            liens.append(lien)
    print(f"{url} : {len(liens)} articles trouvés")
    for l in liens[:3]:
        print("  exemple :", l)
    if liens:
        break

vus = json.load(open(FICHIER)) if os.path.exists(FICHIER) else []
premier_lancement = len(vus) == 0

for lien in reversed(liens):
    if lien not in vus:
        if not premier_lancement:
            requests.post(WEBHOOK, json={"content": f"📰 Nouvelle actu WoW :\n{lien}"})
        vus.append(lien)

json.dump(vus[-200:], open(FICHIER, "w"))
