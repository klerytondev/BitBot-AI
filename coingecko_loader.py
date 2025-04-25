import requests
from datetime import datetime, timedelta

def buscar_cripto_info(consulta: str) -> str:
    consulta = consulta.lower()

    if "preço" in consulta and "últimos 12 meses" in consulta:
        cripto = extrair_nome_cripto(consulta)
        if cripto:
            return historico_preco_12_meses(cripto)
        return "Não consegui identificar a criptomoeda na sua consulta."

    if "preço" in consulta or "cotação" in consulta:
        cripto = extrair_nome_cripto(consulta)
        if cripto:
            return preco_atual(cripto)
        return "Não consegui identificar a criptomoeda na sua consulta."

    return "Não entendi sua consulta sobre criptos. Tente reformular."

def extrair_nome_cripto(consulta: str) -> str:
    # Lista de criptomoedas conhecidas (pode ser expandida ou carregada dinamicamente)
    criptos_conhecidas = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana", "ripple"]
    palavras = consulta.split()
    for palavra in palavras:
        if palavra in criptos_conhecidas:
            return palavra
    return None  # Retorna None se nenhuma criptomoeda for encontrada

def preco_atual(cripto="bitcoin"):
    criptos_conhecidas = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana", "ripple"]
    if cripto not in criptos_conhecidas:
        return f"A criptomoeda '{cripto}' não é suportada no momento."

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies=usd"
    try:
        r = requests.get(url)
        r.raise_for_status()  # Levanta uma exceção para códigos de status HTTP de erro
        data = r.json()
        if cripto in data:
            preco = data[cripto]['usd']
            return f"O preço atual do {cripto.title()} é ${preco} USD."
        return f"Não foi possível encontrar informações de preço para {cripto}."
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API: {e}"

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