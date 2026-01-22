import boto3
import yfinance as yf
import pandas as pd
import json
import os
from io import BytesIO
from datetime import datetime

# Configurações AWS
s3_client = boto3.client('s3')
BUCKET_NAME = "tech-challenge-fiap-bovespa-douglas-varjao"

def load_tickers():

    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base_path, "src", "config", "tickers.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data["tickers"]

def extract():
    # Carrega os tickers: ["PETR4", "BOVA11"] conforme seu tickers.json
    tickers = load_tickers() 
    
    for t in tickers:
        print(f"Iniciando extração de {t}...")
        
        # Realiza o download (ajuste o period conforme necessário)
        df = yf.download(f"{t}.SA", period="5d", interval="1d")
        
        if not df.empty:
            # Reseta o index para que a data vire uma coluna comum
            df.reset_index(inplace=True)
            
            # Normalização de colunas: Resolve o erro de Tupla (MultiIndex) e padroniza em minúsculas
            df.columns = [
                col[0].lower() if isinstance(col, tuple) else col.lower() 
                for col in df.columns
            ]
            
            # Converte a coluna de data para o tipo datetime
            df['date'] = pd.to_datetime(df['date']).dt.floor('ms')

            # Agrupa por data para criar as partições
            for date_val, df_day in df.groupby(df['date'].dt.date):
                date_str = date_val.strftime('%Y-%m-%d')
                
                # Transforma o DataFrame do dia em Parquet na memória
                buffer = BytesIO()
                df_day.to_parquet(buffer, index=False, coerce_timestamps='ms', allow_truncated_timestamps=True)
                
                # Define o caminho no S3 (Key) 
                s3_key = f"raw/ticker={t}/date={date_str}/{t}.parquet"
                
                # Executa o upload para o bucket
                s3_client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=s3_key,
                    Body=buffer.getvalue()
                )
                print(f"✅ Sucesso: {t} enviado para s3://{BUCKET_NAME}/{s3_key}")
        else:
            print(f"⚠️ Nenhum dado encontrado para {t}")

if __name__ == "__main__":
    extract()