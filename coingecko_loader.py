import requests
from datetime import datetime, timedelta

def buscar_cripto_info(consulta: str) -> str:
    consulta = consulta.lower()

    if "preço" in consulta and "últimos 12 meses" in consulta:
        cripto = extrair_nome_cripto(consulta)
        return historico_preco_12_meses(cripto)

    if "preço" in consulta or "cotação" in consulta:
        cripto = extrair_nome_cripto(consulta)
        return preco_atual(cripto)

    return "Não entendi sua consulta sobre criptos. Tente reformular."

def extrair_nome_cripto(consulta: str) -> str:
    # Simplesmente extrai a primeira palavra após "do" ou "da"
    palavras = consulta.split()
    for i, p in enumerate(palavras):
        if p in ["do", "da", "de"]:
            if i+1 < len(palavras):
                return palavras[i+1]
    return "bitcoin"  # fallback

def preco_atual(cripto="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies=usd"
    r = requests.get(url)
    if r.status_code == 200 and cripto in r.json():
        preco = r.json()[cripto]['usd']
        return f"O preço atual do {cripto.title()} é ${preco} USD."
    return f"Não foi possível obter o preço atual do {cripto}."

def historico_preco_12_meses(cripto="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/coins/{cripto}/market_chart?vs_currency=usd&days=365"
    r = requests.get(url)
    if r.status_code == 200 and "prices" in r.json():
        data = r.json()["prices"]
        inicio = datetime.fromtimestamp(data[0][0] / 1000).strftime("%Y-%m-%d")
        fim = datetime.fromtimestamp(data[-1][0] / 1000).strftime("%Y-%m-%d")
        preco_inicio = round(data[0][1], 2)
        preco_fim = round(data[-1][1], 2)
        variacao = round(((preco_fim - preco_inicio) / preco_inicio) * 100, 2)
        return f"De {inicio} a {fim}, o preço do {cripto.title()} variou de ${preco_inicio} para ${preco_fim}, uma variação de {variacao}%."
    return f"Não foi possível obter o histórico de 12 meses para {cripto}."