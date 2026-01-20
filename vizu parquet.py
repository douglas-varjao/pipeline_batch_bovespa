import pandas as pd

# Para ler o arquivo
df = pd.read_parquet('~/Área de trabalho/ML/FASE 2/pipeline_batch_bovespa/ram/data_ingestao=2026-01-12/BOVA11.SA.parquet')

# Para visualizar as primeiras linhas
print(df.head())

# Para ver as informações
print(df.info())
