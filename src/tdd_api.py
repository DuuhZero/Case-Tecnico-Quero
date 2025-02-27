## O código irá conter comentários narrando as etapas do projeto Ass: Eduardo Fontes

import os
import json
import requests
import polars as pl
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

CHAVE_API = 'nrKtyEXrBGMRwcz9xsS4TzaYgd08iUibirrfDF2O' #Esta chave deve ser mudada de acordo com o Token Api do Seu DashBoard do StockData 
URL_BASE = 'https://api.stockdata.org/v1/data/eod'

SIMBOLOS = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BABA', 'V']

# Aqui caso alguem da Quero deseja definir uma data fixa para o teste
data_final = datetime(2024, 2, 23)  # 23/02/2024 (Sexta-feira)
data_inicial = data_final - timedelta(days=14)  # Garante 10 dias úteis

os.makedirs('bronze', exist_ok=True)
os.makedirs('silver', exist_ok=True)
os.makedirs('gold', exist_ok=True)

#Essa função é responsavel para montar a parte Bronze, buscando os dados da API
def buscar_dados(simbolos, data_inicial, data_final, incremental=False):
    for simbolo in simbolos:
        parametros = {
            'symbols': simbolo,
            'api_token': CHAVE_API,
            'date_from': data_inicial.strftime('%Y-%m-%d'),
            'date_to': data_final.strftime('%Y-%m-%d')
        }
        
        resposta = requests.get(URL_BASE, params=parametros)
        
        if resposta.status_code == 200:
            dados = resposta.json().get('data', [])
            if dados:
                caminho_arquivo = f'bronze/{simbolo.lower()}.json'
                modo = 'a' if incremental else 'w'
                
                if modo == 'a' and os.path.exists(caminho_arquivo):
                    with open(caminho_arquivo, 'r+') as arquivo:
                        existente = json.load(arquivo)
                        existente.extend(dados)
                        arquivo.seek(0)
                        json.dump(existente, arquivo)
                else:
                    with open(caminho_arquivo, modo) as arquivo:
                        json.dump(dados, arquivo)
                
                print(f'Dados {"incrementais" if incremental else "iniciais"} de {simbolo} salvos na Pasta Bronze.')
            else:
                print(f'Sem dados para {simbolo}.')
        else:
            print(f'Erro {resposta.status_code} em {simbolo}: {resposta.text}')

def processar_silver(simbolos):
    #Aqui a mágica acontece, transforma os JSON em Parquet
    for simbolo in simbolos:
        caminho_bronze = f'bronze/{simbolo.lower()}.json'
        caminho_prata = f'silver/{simbolo.lower()}.parquet'
        
        if not os.path.exists(caminho_bronze):
            print(f'Arquivo Bronze ausente: {simbolo}')
            continue
            
        df = pl.read_json(caminho_bronze)
        df = df.with_columns(
            pl.col('date').str.slice(0, 10).str.strptime(pl.Date, '%Y-%m-%d').alias('data'),
            pl.lit(simbolo).alias('simbolo')
        )
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        df.write_parquet(caminho_prata)
        print(f'Parquet da pasta Prata processada: {simbolo}')

def processar_gold(simbolos):
    #Aqui a função vai pegar a Parquet ta camada Prata e calcular o preço médio e filtrar últimos 10 dias úteis
    for simbolo in simbolos:
        caminho_prata = f'silver/{simbolo.lower()}.parquet'
        caminho_ouro = f'gold/{simbolo.lower()}.parquet'
        
        if not os.path.exists(caminho_prata):
            print(f' Arquivo Prata ausente: {simbolo}')
            continue
            
        df = pl.read_parquet(caminho_prata)
        df = df.filter(pl.col('data') <= datetime.now().date())  # Filtrar datas futuras
        
        #Garante os últimos 10 dias úteis
        df = df.sort('data', descending=True).head(10)
        
        df_ouro = df.with_columns(
            ((pl.col('open') + pl.col('close')) / 2.0).alias('preco')
        ).select(
            pl.col('simbolo').alias('codigo_acao'),
            'data',
            'preco'
        )
        df_ouro.write_parquet(caminho_ouro)
        print(f'Parquet da pasta Gold processado: {simbolo}')

def atualizar_incremental(simbolos):
    #Aqui o código obtem o preço de cada ação novamente para fazer um incremental do primeiro load
    for simbolo in simbolos:
        entrada = f'silver/{simbolo.lower()}.parquet'
        
        try:
            if os.path.exists(entrada):
                df = pl.read_parquet(entrada)
                ultima_data = df['data'].max()
                nova_data_inicial = ultima_data + timedelta(days=1)
            else:
                nova_data_inicial = datetime.now() - timedelta(days=10)
            
            nova_data_final = datetime.now()
            
            if nova_data_inicial < nova_data_final:
                print(f'Atualizando {simbolo}...')
                buscar_dados([simbolo], nova_data_inicial, nova_data_final, incremental=True)
                processar_silver([simbolo])
                processar_gold([simbolo])
        except Exception as e:
            print(f'Falha na atualização: {e}')

def plotar_precos(simbolos):
    #Aqui vai pegar todos os dados da pasta Gold e plotar no gráfico, sendo possível observar de forma palpavel essas informações
    plt.figure(figsize=(14, 7))
    
    for simbolo in simbolos:
        caminho_ouro = f'gold/{simbolo.lower()}.parquet'
        
        if os.path.exists(caminho_ouro):
            df = pl.read_parquet(caminho_ouro)
            df = df.sort('data')
            
            plt.plot(
                df['data'].to_list(),
                df['preco'].to_list(),
                marker='o',
                linestyle='-',
                label=simbolo
            ) 
    
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m'))
    plt.gcf().autofmt_xdate()
    
    plt.title('Preço Médio Diário - Últimos 10 Dias Úteis', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Preço (USD)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show() #Aqui basicamente setei as colunas X, Y, legendas, tamanho da font e etc.


if __name__ == "__main__":
    print("Iniciando pipeline...\n")
    
    print("1. Carregando dados iniciais...")
    buscar_dados(SIMBOLOS, data_inicial, data_final)
    
    print("\n2. Processando camada Prata...")
    processar_silver(SIMBOLOS)
    
    print("\n3. Processando camada Ouro...")
    processar_gold(SIMBOLOS)
    
    print("\n4. Gerando gráfico...")
    plotar_precos(SIMBOLOS)
    
    print("\nPipeline concluído!")