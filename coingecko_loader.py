import requests

def buscar_cripto_info(cripto="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies=usd"
    r = requests.get(url)
    return r.json()