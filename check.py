import os, json, re, html, requests

URLS = [
    "https://news.blizzard.com/fr-fr/feed/world-of-warcraft",
    "https://news.blizzard.com/en-us/feed/world-of-warcraft",
]
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
FICHIER = "seen.json"

def nettoie(t):
    t = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", t or "", flags=re.S)
    return html.unescape(t).strip()

actus = []
for url in URLS:
    texte = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
    print("Début du flux :", texte[:300])
    for bloc in re.findall(r"<(?:item|entry)\b.*?>(.*?)</(?:item|entry)>", texte, flags=re.S):
        titre = re.search(r"<title[^>]*>(.*?)</title>", bloc, flags=re.S)
        lien = re.search(r'<link[^>]*href="([^"]+)"', bloc) or re.search(r"<link>(.*?)</link>", bloc, flags=re.S)
        if titre and lien:
            actus.append((nettoie(lien.group(1)), nettoie(titre.group(1))))
    print(f"{url} : {len(actus)} actus trouvées")
    if actus:
        break

vus = json.load(open(FICHIER)) if os.path.exists(FICHIER) else []
premier_lancement = len(vus) == 0

for lien, titre in reversed(actus):
    if lien not in vus:
        if not premier_lancement:
            requests.post(WEBHOOK, json={"content": f"📰 **{titre}**\n{lien}"})
        vus.append(lien)

json.dump(vus[-200:], open(FICHIER, "w"))
