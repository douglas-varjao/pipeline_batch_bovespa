import yfinance as yf
import pandas as pd
from datetime import datetime
import os

#1. definir o ticker de interesse
ticker = "BOVA11.SA"
hoje = datetime.now().strftime("%Y-%m-%d")


df = yf.download(simbolo, period="1d", interval="1d")
#2. extrai dados

if not df.empty:
    df = df.reset_index()

    df.columns = [col[0].lower() in isinstance(col, tuple) else col.lower() for col in df.columns]

    path = f"raw/data_ingestao={hoje}"
    os.makedirs(diretorio_particao, exist_ok=True)



def extrair_bovespa(simbolo):
    
    return df

dados = extrair_bovespa(ticker)

if not dados.empty:
    diretorio_particao = f"raw/data_ingestao={hoje}"
    os.makedirs(diretorio_particao, exist_ok=True)

    caminho_arquivo = f"{diretorio_particao}/{ticker}.parquet"
    dados.to_parquet(caminho_arquivo, index=True)

    print(f"Sucesso! Dados de {ticker} salvos em {caminho_arquivo}")
 