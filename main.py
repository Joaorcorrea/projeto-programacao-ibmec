#link para acessar a pasta com todos os arquivos do código: https://github.com/Joaorcorrea/projeto-programacao-ibmec/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#variável para o caminho da planilha
dados = "trabalho programacao.xls"
#cria o dicionario dos ativos publicos e privados
publicos = {'NTN-B 760199': [], 'NTN-C770100':[], 'NTN-F950199': [], 'LTN 100000': [], 'LFT210100': []}
privados = {'TVVH11': [], 'RDCO34':[], 'RIPR': [], 'CRMG15': [], 'VALE28': []}

#Pegando os dados dos títulos privados da planilha e colocando dentro do dicionario
dados_f = pd.read_excel(dados, sheet_name='PRIVADAS', usecols='C', skiprows=1).dropna()['Taxa (YTM)'].iloc[1:253]
privados['TVVH11'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PRIVADAS', usecols='F', skiprows=1).dropna()['Taxa (YTM).1'].iloc[1:253]
privados['RDCO34'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PRIVADAS', usecols='I', skiprows=1).dropna()['Taxa (YTM).2'].iloc[1:253]
privados['RIPR'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PRIVADAS', usecols='L', skiprows=1).dropna()['Taxa (YTM).3'].iloc[1:253]
privados['CRMG15'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PRIVADAS', usecols='O', skiprows=1).dropna()['Taxa (YTM).4'].iloc[1:253]
privados['VALE28'] = dados_f.tolist()

#Pegando os dados dos titulos publicos da planilha e coloque dentro do dicionário
dados_f = pd.read_excel(dados, sheet_name='PUBLICO', usecols='C', skiprows=1).dropna()['Taxa (YTM)'].iloc[1:250]
publicos['NTN-B 760199'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PUBLICO', usecols='F', skiprows=1).dropna()['Taxa (YTM).1'].iloc[1:250]
publicos['NTN-C770100'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PUBLICO', usecols='I', skiprows=1).dropna()['Taxa (YTM).2'].iloc[1:250]
publicos['NTN-F950199'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PUBLICO', usecols='L', skiprows=1).dropna()['Taxa (YTM).3'].iloc[1:250]
publicos['LTN 100000'] = dados_f.tolist()
dados_f = pd.read_excel(dados, sheet_name='PUBLICO', usecols='O', skiprows=1).dropna()['Taxa (YTM).4'].iloc[1:250]
publicos['LFT210100'] = dados_f.tolist()

#Função para calcular os Coeficientes de Variação para os títulos publicos e privados
def coeficiente_variacao(retornos):
    #Inicializa um dionário para adicionar os coeficientes
    resultado_coeficiente_variacao = {}

    #Para cada título, fazer os cálculos baseados em seus retornos diários. No caso retornos é uma variável, para diferenciar os públicos dos privados.
    for titulo in retornos:
        # Acessar a lista de retornos diários para o ativo 'PETR27'
        retorno = retornos[titulo]

        # Calculo das variacoes
        variacao = np.diff(retorno) / retorno[:-1]

        #Média
        media = np.mean(variacao)

        #Desvido padrão
        desvio_p = np.std(variacao)

        #Faz calculo do Coeficiente de Variação Pearson
        cv = (desvio_p/media)

        #Verificar se o coeficiente é positivo, se sim, adiciona ao dicionario
        if cv > 0:
            resultado_coeficiente_variacao[titulo] = {"Média": media, "DP": desvio_p, "CV": cv}

    #Retorna o dicionario com os CVs calculados
    return resultado_coeficiente_variacao

#Monta dicionários de duas carteiras com base nos menores Coeficientes de Variação de Pearson, uma para públicos e outra para privados.
#carteira de titulos publicos
cv_publicos = coeficiente_variacao(publicos)#cria dicionarios para os coeficientes positivos de titulos publicos
publicos_ordenados = sorted(cv_publicos.items(), key=lambda x: x[1]['CV'])# Ordena os títulos com base no coeficiente de variação
carteira_publicos = dict(publicos_ordenados[:2])#Seleciona os titulos com os dois menores coeficientes de variação

#carteira de titulos privados
cv_privados = coeficiente_variacao(privados)#cria dicionarios para os coeficientes positivos de titulos privados
privados_ordenados = sorted(cv_privados.items(), key=lambda x: x[1]['CV'])# Ordena os títulos com base no coeficiente de variação
carteira_privados = dict(privados_ordenados[:2])#Seleciona os titulos com os dois menores coeficientes de variação

#Função para calcular o indice sharpe e do peso de cada título selecionado na carteira privada.
def sharpe_pr():
    # Taxa de retorno livre de risco
    rf = 0.03
    
    # Inicializando variáveis para armazenar a melhor combinação de pesos e maior Sharpe
    global p_privados
    maior_sharpe = float('-inf')

# Testando diferentes combinações de pesos
    for peso_rdco34 in range(0, 101, 2):  # Variação de 2% em 2%
        peso_crmg15 = 100 - peso_rdco34  # O restante é o peso para o outro título

        # Convertendo os pesos para a escala de 0 a 1.0
        peso_rdco34 = peso_rdco34 / 100
        peso_crmg15 = peso_crmg15 / 100

        # Calculando o retorno médio da carteira
        m_portf = (float(carteira_privados['RDCO34']['Média']) * peso_rdco34) + (float(carteira_privados['CRMG15']['Média']) * peso_crmg15)

        # Calculando o desvio padrão da carteira
        dp_portf = ((float(carteira_privados['RDCO34']['DP']) ** 2) * (peso_rdco34 ** 2) + (float(carteira_privados['CRMG15']['DP']) ** 2) * (peso_crmg15 ** 2)) ** 0.5

        # Calculando o índice de Sharpe
        sharpe = (m_portf - rf) / dp_portf

        # Atualizando a melhor combinação de pesos para cada título e maior Sharpe
        if sharpe > maior_sharpe:
            p_privados = {'RDCO34': peso_rdco34, 'CRMG15': peso_crmg15}
            maior_sharpe = sharpe
    return p_privados


#Cálculo do indice sharpe e do peso de cada título selecionado na carteira pública.
def sharpe_pu():
    # Taxa de retorno livre de risco 
    rf = 0.03
    
    # Inicializando variáveis para armazenar a melhor combinação de pesos e maior Sharpe
    global p_publico
    maior_sharpe = float('-inf')

# Testando diferentes combinações de pesos
    for peso_lft in range(0, 101, 2):  # Variação de 2% em 2%
        peso_ntn = 100 - peso_lft  # O restante é o peso para o outro titulo

        # Convertendo os pesos para a escala de 0 a 1.0
        peso_lft = peso_lft / 100
        peso_ntn = peso_ntn / 100

        # Calculando o retorno médio da carteira
        m_portf = (float(carteira_publicos['LFT210100']['Média']) * peso_lft) + (float(carteira_publicos['NTN-B 760199']['Média']) * peso_ntn)

        # Calculando o desvio padrão da carteira
        dp_portf = ((float(carteira_publicos['LFT210100']['DP']) ** 2) * (peso_lft ** 2) + (float(carteira_publicos['NTN-B 760199']['DP']) ** 2) * (peso_ntn ** 2)) ** 0.5

        # Calculando o índice de Sharpe
        sharpe = (m_portf - rf) / dp_portf

        # Atualizando a melhor combinação de pesos e maior Sharpe
        if sharpe > maior_sharpe:
            p_publico = {'LFT210100': peso_lft, 'NTN-B 760199': peso_ntn}
            maior_sharpe = sharpe

    return p_publico


#Funções para cálculo de retornos das carteiras e faz a criação dos gráficos de comparação
def r_carteira_publica(investimento):
    #Chamando a função que faz os cálculos de sharpe e peso para calcular os retornos anteriores da carteira
    sharpe_pu()
    #Cálculo para retornos anteriores da carteira baseado no peso de cada título público
    r_total_anterior = ((p_publico['LFT210100']*(0.0155736)) + (p_publico['NTN-B 760199']*(2.34)))
    r_esperado = round((p_publico['LFT210100']*(12.25)+p_publico['NTN-B 760199']*(6.83+5.19)),2)
    r_investido = round(investimento*(r_esperado/100 + 1), 2)
    print(f"\nCARTEIRA DE TÍTULOS PÚBLICOS\nAtivos: LFT210100 NTN-B 760199\nInvestimento: R${investimento}\nPeso de cada ativo: LFT210100: {p_publico['LFT210100']*100}% e NTN-B 760199: {p_publico['NTN-B 760199']*100}%\nRetorno esperado: {r_esperado}%\nRetorno Anterior: {r_total_anterior}%\nMontante final(Baseado no Retorno Estimado): R${r_investido}\n")

    # Valores dos índices de comparação
    cdi_esperado = 9.15
    selic_esperada = 10.07
    ipca_esperado = 3.90

    #definindo a largura das barras do gráfico
    largura = 0.35

    #definindo os índices dos elementos para posicionar as barras no gráfico
    r1 = range(len(['CARTEIRA PÚBLICOS', 'SELIC', 'CDI', 'IPCA']))
    #Configurando a barra do gráfico(posição), valores, cor, largura e legenda
    plt.bar(r1, [r_esperado, selic_esperada, cdi_esperado, ipca_esperado], color='blue', width=largura, label='Retorno Esperado')
    #Título do gráfico
    plt.title('Comparação de Retornos (Carteira de Títulos Públicos)')
    #Título do eixo x e peso da fonte
    plt.xlabel('Indicadores', fontweight='bold')
    #Título do eixo y e peso da fonte
    plt.ylabel('Retorno (%)', fontweight='bold')
    #Ajusta os rótulos de cada barra em suas devidas posiçoes
    plt.xticks(r1, ['CARTEIRA PÚBLICOS', 'SELIC', 'CDI', 'IPCA'])
    #Aciona as legendas
    plt.legend()
    
    #inicia os gráficos
    plt.show()

def r_carteira_privada(investimento):
    #Chamando a função que faz os cálculos de sharpe e peso para calcular os retornos anteriores da carteira
    sharpe_pr()

    #Cálculo para retornos anteriores e esperados da carteira baseado no peso de cada título privado
    r_total_anterior = round((p_privados['RDCO34']*(2.48+13.41)) + (p_privados['CRMG15']*5.19+7.38)/2, 2)
    r_esperado = round(p_privados['RDCO34']*(1.9652+13.41) + (p_privados['CRMG15']*(5.19+7.42))/2, 2)
    r_investido = round(investimento*(r_esperado/100 + 1), 2)
    print(f"\nCARTEIRA DE TÍTULOS PRIVADOS\nAtivos: CONCESS DA RODOVIA MG 05, RODIVAS DAS COLINAS AS\nInvestimento: R${investimento}\nPeso de cada ativo: CRMG15: {p_privados['CRMG15']*100}% e RDCO34: {p_privados['RDCO34']*100}%\nRetorno esperado: {r_esperado}%\nRetorno Anterior: {r_total_anterior}%\nMontante final: R${r_investido}\n")

    # Valores esperados dos índices de comparação
    cdi_esperado = 9.97
    selic_esperada = 10.07
    ipca_esperado = 3.90

    #definindo rótulos do gráfico
    valores = ['CARTEIRA PRIVADA', 'SELIC', 'CDI', 'IPCA']

    #definindo a largura das barras do gráfico
    largura = 0.35

    #definindo os índices dos elementos para posicionar as barras no gráfico
    r1 = range(len(valores))
    #Configurando a barra do gráfico(posição), valores, cor, largura e legenda
    plt.bar(r1, [r_esperado, selic_esperada, cdi_esperado, ipca_esperado], color='green', width=largura, label='Retorno Esperado')
    #Título do gráfico
    plt.title('Comparação de Retornos (Carteira Títulos Privados')
    #Título do eixo x e peso da fonte
    plt.xlabel('Indicadores', fontweight='bold')
    #Título do eixo y e peso da fonte
    plt.ylabel('Retorno (%)', fontweight='bold')
    #Ajusta os rótulos de cada barra em suas devidas posiçoes
    plt.xticks(r1, valores)
    #Aciona as legendas
    plt.legend()
    #inicia os gráficos
    plt.show()

investimento = float(input("Digite o valor a ser investido: "))
r_carteira_publica(investimento)
r_carteira_privada(investimento)
