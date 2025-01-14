import csv
from sys import argv

import pandas as pd
import seaborn as sns

df = pd.read_csv('./taxa-cdi.csv')

grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticks(range(len(df['hora'])))
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)

# Usar um argumento padrão se nenhum for fornecido
output_filename = argv[1] if len(argv) > 1 else 'grafico.png'
grafico.get_figure().savefig(output_filename)