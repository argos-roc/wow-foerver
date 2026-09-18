import os
import requests
from bs4 import BeautifulSoup

URL = "https://eu.gear.blizzard.com/products/wowccl0014-french-ce"
WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/18.0 Mobile/15E148 Safari/604.1"
    )
}

response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Vérification que nous sommes bien sur la Collector française
title = soup.get_text(" ", strip=True)

if "World of Warcraft: Forever Collector's Edition - French" not in title:
    raise Exception("Impossible de confirmer la page Collector française.")

# Recherche des indicateurs de disponibilité
page_text = title.lower()

sold_out = "sold out" in page_text
preorder = "pre-order" in page_text or "pré-commande" in page_text

# On considère disponible uniquement si la page n'indique PAS "Sold out"
# ET qu'un bouton d'achat est présent.
buy_button = soup.find(
    lambda tag: tag.name in ["button", "input"]
    and (
        "add to cart" in tag.get_text(" ", strip=True).lower()
        or "add to cart" in str(tag).lower()
    )
)

available = not sold_out and buy_button is not None

print(f"Collector française détectée : oui")
print(f"Sold out : {sold_out}")
print(f"Précommande : {preorder}")
print(f"Bouton d'achat détecté : {buy_button is not None}")
print(f"Disponible : {available}")

if available:
    message = (
        "🚨🚨 **WOW FOREVER COLLECTOR FRANÇAISE DISPONIBLE !** 🚨🚨\n\n"
        "🇫🇷 Édition française\n"
        "💰 Prix officiel : 150 €\n\n"
        f"👉 **ACHETER :** {URL}"
    )

    requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=30
    ).raise_for_status()

    print("✅ Alerte Discord envoyée !")
else:
    print("❌ Pas disponible actuellement.")
