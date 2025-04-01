import csv
from datetime import datetime
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Union

def carregar_dados(nome_arquivo: str) -> List[Dict]:
    """
    Carrega dados meteorológicos do arquivo CSV para uma lista de dicionários.
    Cada dicionário contém os dados de um dia.
    """
    dados = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)  # Pula a linha do cabeçalho
            for linha in leitor:
                if len(linha) >= 6:  # Garante que a linha tem todos os campos necessários
                    dados.append({
                        'data': datetime.strptime(linha[0], '%d/%m/%Y'),
                        'precipitacao': float(linha[1]),
                        'temp_max': float(linha[2]),
                        'temp_min': float(linha[3]),
                        'umidade': float(linha[4]),
                        'vento': float(linha[5])
                    })
    except FileNotFoundError:
        print(f"Erro: Arquivo {nome_arquivo} não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")
        return []
    return dados

def validar_intervalo_datas(dados: List[Dict], mes_inicio: int, ano_inicio: int, 
                          mes_fim: int, ano_fim: int) -> bool:
    """Valida se o intervalo de datas é válido e existe nos dados."""
    if not (1 <= mes_inicio <= 12 and 1 <= mes_fim <= 12):
        return False
    if not (1961 <= ano_inicio <= 2016 and 1961 <= ano_fim <= 2016):
        return False
    if ano_inicio > ano_fim or (ano_inicio == ano_fim and mes_inicio > mes_fim):
        return False
    return True

def visualizar_dados(dados: List[Dict], mes_inicio: int, ano_inicio: int,
                    mes_fim: int, ano_fim: int, tipo_visualizacao: int) -> None:
    """Exibe os dados de acordo com o intervalo e tipo de visualização especificados pelo usuário."""
    if not validar_intervalo_datas(dados, mes_inicio, ano_inicio, mes_fim, ano_fim):
        print("Intervalo de datas inválido!")
        return

    data_inicio = datetime(ano_inicio, mes_inicio, 1)
    data_fim = datetime(ano_fim, mes_fim, 1)

    print("\nDados do período solicitado:")
    if tipo_visualizacao == 1:
        print("Data\t\tPrecipitação\tTemp. Máx\tTemp. Mín\tUmidade\tVento")
        print("-" * 70)
    elif tipo_visualizacao == 2:
        print("Data\t\tPrecipitação")
        print("-" * 25)
    elif tipo_visualizacao == 3:
        print("Data\t\tTemp. Máx\tTemp. Mín")
        print("-" * 40)
    elif tipo_visualizacao == 4:
        print("Data\t\tUmidade\tVento")
        print("-" * 30)

    for registro in dados:
        if data_inicio <= registro['data'] <= data_fim:
            if tipo_visualizacao == 1:
                print(f"{registro['data'].strftime('%d/%m/%Y')}\t{registro['precipitacao']:.1f}\t\t{registro['temp_max']:.1f}\t\t{registro['temp_min']:.1f}\t\t{registro['umidade']:.1f}\t{registro['vento']:.1f}")
            elif tipo_visualizacao == 2:
                print(f"{registro['data'].strftime('%d/%m/%Y')}\t{registro['precipitacao']:.1f}")
            elif tipo_visualizacao == 3:
                print(f"{registro['data'].strftime('%d/%m/%Y')}\t{registro['temp_max']:.1f}\t\t{registro['temp_min']:.1f}")
            elif tipo_visualizacao == 4:
                print(f"{registro['data'].strftime('%d/%m/%Y')}\t{registro['umidade']:.1f}\t{registro['vento']:.1f}")

def mes_mais_chuvoso(dados: List[Dict]) -> Tuple[str, float]:
    """Encontra o mês/ano com maior precipitação."""
    precipitacao_por_mes = {}
    
    for registro in dados:
        mes_ano = registro['data'].strftime('%B/%Y')
        if mes_ano not in precipitacao_por_mes:
            precipitacao_por_mes[mes_ano] = 0
        precipitacao_por_mes[mes_ano] += registro['precipitacao']
    
    mes_mais_chuvoso = max(precipitacao_por_mes.items(), key=lambda x: x[1])
    return mes_mais_chuvoso

def media_temp_minima_mes(dados: List[Dict], mes: int) -> Dict[str, float]:
    """Calcula a média da temperatura mínima para um determinado mês entre 2006-2016."""
    if not (1 <= mes <= 12):
        return {}
    
    medias_por_ano = {}
    for registro in dados:
        if 2006 <= registro['data'].year <= 2016 and registro['data'].month == mes:
            chave = f"{registro['data'].strftime('%B')}{registro['data'].year}"
            if chave not in medias_por_ano:
                medias_por_ano[chave] = []
            medias_por_ano[chave].append(registro['temp_min'])
    
    # Calcula as médias
    for chave in medias_por_ano:
        medias_por_ano[chave] = sum(medias_por_ano[chave]) / len(medias_por_ano[chave])
    
    return medias_por_ano

def plotar_media_temp_minima(medias: Dict[str, float], mes: int) -> None:
    """Cria um gráfico de barras com as médias de temperatura mínima."""
    anos = [chave[-4:] for chave in medias.keys()]
    temperaturas = list(medias.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(anos, temperaturas, color='skyblue')
    plt.title(f'Média de Temperatura Mínima - {mes} (2006-2016)')
    plt.xlabel('Ano')
    plt.ylabel('Temperatura Mínima Média (°C)')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.show()

def main():
    # Carrega os dados
    dados = carregar_dados('Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv')
    if not dados:
        return

    while True:
        print("\nMenu Principal:")
        print("1. Visualizar dados por período")
        print("2. Mostrar mês mais chuvoso")
        print("3. Calcular média de temperatura mínima por mês")
        print("4. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            try:
                mes_inicio = int(input("Mês inicial (1-12): "))
                ano_inicio = int(input("Ano inicial (1961-2016): "))
                mes_fim = int(input("Mês final (1-12): "))
                ano_fim = int(input("Ano final (1961-2016): "))
                
                print("\nTipo de visualização:")
                print("1. Todos os dados")
                print("2. Apenas precipitação")
                print("3. Apenas temperatura")
                print("4. Apenas umidade e vento")
                tipo_visualizacao = int(input("Escolha o tipo de visualização: "))
                
                if 1 <= tipo_visualizacao <= 4:
                    visualizar_dados(dados, mes_inicio, ano_inicio, mes_fim, ano_fim, tipo_visualizacao)
                else:
                    print("Opção de visualização inválida!")
            except ValueError:
                print("Por favor, insira valores numéricos válidos!")
                
        elif opcao == '2':
            mes, precipitacao = mes_mais_chuvoso(dados)
            print(f"\nMês mais chuvoso: {mes}")
            print(f"Precipitação total: {precipitacao:.2f} mm")
            
        elif opcao == '3':
            try:
                mes = int(input("Digite o mês (1-12): "))
                medias = media_temp_minima_mes(dados, mes)
                
                if medias:
                    print("\nMédias de temperatura mínima por ano:")
                    for chave, media in medias.items():
                        print(f"{chave}: {media:.2f}°C")
                    
                    media_geral = sum(medias.values()) / len(medias)
                    print(f"\nMédia geral: {media_geral:.2f}°C")
                    
                    plotar_media_temp_minima(medias, mes)
                else:
                    print("Mês inválido ou sem dados disponíveis!")
            except ValueError:
                print("Por favor, insira um número válido!")
                
        elif opcao == '4':
            print("Programa encerrado!")
            break
            
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main() 