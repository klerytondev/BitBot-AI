import requests

url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum",  # IDs das moedas separadas por vírgula
    "vs_currencies": "usd,brl"  # Moedas fiduciárias
}

response = requests.get(url, params=params)
data = response.json()
print(data)
# Saída exemplo: {'bitcoin': {'usd': 65000, 'brl': 330000}, 'ethereum': {'usd': 3500, 'brl': 18000}}
