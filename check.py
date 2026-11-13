import os, json, requests
import xml.etree.ElementTree as ET

URL = "https://news.blizzard.com/fr-fr/feed/world-of-warcraft"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
FICHIER = "seen.json"

xml = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).content
items = ET.fromstring(xml).findall(".//item")
actus = [(i.findtext("link"), i.findtext("title")) for i in items]
print(f"{len(actus)} actus trouvées")

vus = json.load(open(FICHIER)) if os.path.exists(FICHIER) else []
premier_lancement = len(vus) == 0

for lien, titre in reversed(actus):
    if lien not in vus:
        if not premier_lancement:
            requests.post(WEBHOOK, json={"content": f"📰 **{titre}**\n{lien}"})
        vus.append(lien)

json.dump(vus[-200:], open(FICHIER, "w"))
