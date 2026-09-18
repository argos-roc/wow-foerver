import os
import requests
from bs4 import BeautifulSoup

URL = "https://eu.gear.blizzard.com/products/wowccl0014-french-ce"
WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1"
}

response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text(" ", strip=True).lower()

# On vérifie qu'il s'agit bien de l'édition française
if "world of warcraft: forever collector's edition - french" not in text:
    raise Exception("La page française n'a pas été trouvée.")

# Blizzard affiche actuellement "Sold out" quand elle n'est plus disponible.
sold_out = "sold out" in text

if not sold_out:
    message = (
        "🚨 **WOW FOREVER COLLECTOR FRANÇAISE DISPONIBLE !** 🚨\n\n"
        "💰 Prix attendu : 150 €\n"
        "🇫🇷 Édition française\n\n"
        f"👉 ACHETER MAINTENANT : {URL}"
    )

    requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=20
    )

    print("🚨 ALERTE DISCORD ENVOYÉE !")
else:
    print("❌ Toujours en rupture.")