import csv
import json
import os
import time
from datetime import datetime
from random import random
from sys import argv

import pandas as pd
import requests
import seaborn as sns

# URL da API do Banco Central para pegar a taxa CDI
URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# Função para extrair a taxa CDI do site
def extrair_taxa_cdi():
    try:
        response = requests.get(url=URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        return None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        return json.loads(response.text)[-1]['valor']

# Função para gerar e salvar o CSV com dados da taxa CDI
def gerar_csv():
    dado = extrair_taxa_cdi()

    for _ in range(0, 10):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

        cdi = float(dado) + (random() - 0.5)

        # Verificando se o arquivo "taxa-cdi.csv" existe
        if not os.path.exists('./taxa-cdi.csv'):
            with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n')

        # Salvando dados no arquivo "taxa-cdi.csv"
        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(1)

    print("CSV gerado com sucesso.")

# Função para gerar e salvar o gráfico
def gerar_grafico(nome_grafico):
    df = pd.read_csv('./taxa-cdi.csv')

    # Criando o gráfico de linha
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{nome_grafico}.png")
    print(f"Gráfico salvo como {nome_grafico}.png")

# Função principal que executa as tarefas
def main():
    if len(argv) < 2:
        print("Por favor, forneça o nome do gráfico como parâmetro.")
        return

    nome_grafico = argv[1]

    # Gerar o CSV com os dados da taxa CDI
    gerar_csv()

    # Gerar o gráfico com o nome fornecido
    gerar_grafico(nome_grafico)

if __name__ == "__main__":
    main()
