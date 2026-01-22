import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path
from src.utils.helpers import load_tickers
import os
import sys

def extract():
    try:
        tickers = load_tickers()
        base_raw_path = Path("data","raw")

        for t in tickers:
            print(f"Processando {t}... em {base_raw_path}")
            df = yf.download(f"{t}.SA", period="5d", interval="1d")

            if not df.empty:
                df.reset_index(inplace=True)
                df.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in df.columns]

                for date_val, df_day in df.groupby('date'):
                    date_str = date_val.strftime('%Y-%m-%d')
                    output_dir = base_raw_path / f"ticker={t}" / f"date={date_str}"
                    output_dir.mkdir(parents=True, exist_ok=True)

                    df_day.to_parquet(output_dir/f"{t}.parquet", index=False)
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        
if __name__ == "__main__":
    extract()