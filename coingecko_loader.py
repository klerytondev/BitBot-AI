import requests
from datetime import datetime, timedelta

def buscar_cripto_info(consulta: str) -> dict:
    consulta = consulta.lower()

    if "preço" in consulta and "últimos 12 meses" in consulta:
        cripto = extrair_nome_cripto(consulta)
        if cripto["sucesso"]:
            return {
                "consulta": consulta,
                "tipo": "historico_preco_12_meses",
                "resultado": historico_preco_12_meses(cripto["nome"])
            }
        return {
            "consulta": consulta,
            "tipo": "historico_preco_12_meses",
            "erro": "Não consegui identificar a criptomoeda na sua consulta."
        }

    if "preço" in consulta or "cotação" in consulta:
        cripto = extrair_nome_cripto(consulta)
        if cripto["sucesso"]:
            return {
                "consulta": consulta,
                "tipo": "preco_atual",
                "resultado": preco_atual(cripto["nome"])
            }
        return {
            "consulta": consulta,
            "tipo": "preco_atual",
            "erro": "Não consegui identificar a criptomoeda na sua consulta."
        }

    return {
        "consulta": consulta,
        "tipo": "indefinido",
        "erro": "Não entendi sua consulta sobre criptos. Tente reformular."
    }

def extrair_nome_cripto(consulta: str) -> dict:
    criptos_conhecidas = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana", "ripple"]
    palavras = consulta.split()
    for palavra in palavras:
        if palavra in criptos_conhecidas:
            return {
                "sucesso": True,
                "nome": palavra
            }
    return {
        "sucesso": False,
        "erro": "Nenhuma criptomoeda conhecida foi encontrada na consulta."
    }

def preco_atual(cripto="bitcoin"):
    criptos_conhecidas = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana", "ripple"]
    if cripto not in criptos_conhecidas:
        return {"erro": f"A criptomoeda '{cripto}' não é suportada no momento."}

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies=usd"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        if cripto in data:
            preco = data[cripto]['usd']
            return {
                "criptomoeda": cripto,
                "preco_atual_usd": preco,
                "mensagem": f"O preço atual do {cripto.title()} é ${preco} USD."
            }
        return {"erro": f"Não foi possível encontrar informações de preço para {cripto}."}
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao acessar a API: {e}"}

def historico_preco_12_meses(cripto="bitcoin"):
    criptos_conhecidas = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana", "ripple"]
    if cripto not in criptos_conhecidas:
        return {"erro": f"A criptomoeda '{cripto}' não é suportada no momento."}

    url = f"https://api.coingecko.com/api/v3/coins/{cripto}/market_chart?vs_currency=usd&days=365"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        if "prices" in data:
            prices = data["prices"]
            if len(prices) < 2:
                return {"erro": f"Dados insuficientes para calcular o histórico de 12 meses para {cripto}."}

            inicio = datetime.fromtimestamp(prices[0][0] / 1000).strftime("%Y-%m-%d")
            fim = datetime.fromtimestamp(prices[-1][0] / 1000).strftime("%Y-%m-%d")
            preco_inicio = round(prices[0][1], 2)
            preco_fim = round(prices[-1][1], 2)

            if preco_inicio == 0:
                return {"erro": f"Não foi possível calcular a variação percentual para {cripto} devido a dados inválidos."}

            variacao = round(((preco_fim - preco_inicio) / preco_inicio) * 100, 2)
            return {
                "criptomoeda": cripto,
                "periodo": {"inicio": inicio, "fim": fim},
                "preco_inicio_usd": preco_inicio,
                "preco_fim_usd": preco_fim,
                "variacao_percentual": variacao,
                "mensagem": f"De {inicio} a {fim}, o preço do {cripto.title()} variou de ${preco_inicio} para ${preco_fim}, uma variação de {variacao}%."
            }
        return {"erro": f"Não foi possível obter o histórico de 12 meses para {cripto}."}
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao acessar a API: {e}"}