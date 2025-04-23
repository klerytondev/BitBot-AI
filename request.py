import requests

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "30"
}

response = requests.get(url, params=params)
data = response.json()
print(data['prices'])  # Lista de pares [timestamp, preço]
