# import requests
# import csv
# import os
# from datetime import datetime

# moedas = ['bitcoin', 'ethereum', 'solana', 'cardano', 'ripple']
# dados_todos = []

# # Garante que a pasta 'data' existe
# os.makedirs('data', exist_ok=True)

# for moeda in moedas:
#     url = f'https://api.coingecko.com/api/v3/coins/{moeda}/market_chart'
#     params = {
#         'vs_currency': 'usd',  # Pegamos USD primeiro
#         'days': '365'
#     }
#     response_usd = requests.get(url, params=params)
    
#     params['vs_currency'] = 'brl'  # Agora pegamos BRL
#     response_brl = requests.get(url, params=params)
    
#     if response_usd.status_code == 200 and response_brl.status_code == 200:
#         dados_usd = response_usd.json()['prices']
#         dados_brl = response_brl.json()['prices']
        
#         # Assume que ambas as listas têm os mesmos timestamps e ordem
#         for (timestamp_usd, preco_usd), (timestamp_brl, preco_brl) in zip(dados_usd, dados_brl):
#             data = datetime.fromtimestamp(timestamp_usd // 1000).strftime('%Y-%m-%d')
#             dados_todos.append([moeda, data, preco_usd, preco_brl])
#         print(f'Dados de {moeda} coletados.')
#     else:
#         print(f'Erro ao buscar dados de {moeda}: USD {response_usd.status_code}, BRL {response_brl.status_code}')

# # Ordena os dados por moeda e data
# dados_todos.sort(key=lambda x: (x[0], x[1]))

# # Salva em um único CSV na pasta 'data'
# caminho_arquivo = os.path.join('data', 'historico_criptomoedas.csv')
# with open(caminho_arquivo, 'w', newline='') as arquivo:
#     writer = csv.writer(arquivo)
#     writer.writerow(['moeda', 'data', 'preco_usd', 'preco_brl'])
#     writer.writerows(dados_todos)

# print(f'Arquivo {caminho_arquivo} gerado com sucesso!')
