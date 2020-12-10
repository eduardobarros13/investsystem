
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import yfinance
import pandas_datareader.data as web
import requests
import pandas as pd
import time
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import sqlite3

###############Criando telas de logins###################
#@academia_required(login_url='/login/')

@login_required(login_url='/login/')
def academia(request):
    data ={}
    return render(request, 'contas/academia.html', data)

    
def logout_user(request):
    logout(request)
    return redirect('/login/')


def logado(request):
    return render (request, 'logado.html')


def login_user(request):
    logout(request)
    return render(request,'login.html')

@csrf_protect 
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('/home1/')
        else:
            messages.error(request, 'Usuario e senha invalidos. favor tentar novamente.')
    return redirect('/login/')
    
################################
###########Dados de coleta dos robos###############

@login_required(login_url='/login/')
def put(request):
    while True:
        data = {}
        banco = pd.read_excel('InvestSystem3.0_django.xlsm',
                                   sheet_name='Rastreador_PUT',header=8)

        banco['Strike VS Cot. (%)'] = pd.to_numeric(banco['Strike VS Cot. (%)']*100, errors='coerce')
        banco['TIR (%)'] = pd.to_numeric(banco['TIR (%)']*100, errors='coerce')
        banco['VENC.'] = pd.to_datetime(banco['VENC.'], errors='coerce')
        banco['VENC.'] = banco['VENC.'].dt.strftime("%d/%m/%Y")

        banco['Strike VS Cot. (%)'] = round(banco['Strike VS Cot. (%)'], 2)
        banco['TIR (%)'] = round(banco['TIR (%)'], 2)

        data['PUT'] = banco['STRIKE']       
        data['ATIVO'] = banco['ATIVO']
        data['PRECO'] = banco['Real Time']
        data['RASTREADOR'] = banco['Robo PUT']
        data['VENCIMENTO'] = banco['VENC.']

        data['TIR'] = banco['TIR (%)']
        data['PROTECAO'] = banco['Strike VS Cot. (%)']
        data['Negocios'] = banco['Negocios']

        return render(request, 'contas/home.html', data)
    time.sleep(6*5)

@login_required(login_url='/login/')
def news(request):
    data={}
    
    #news = pd.read_excel('C:/Users/Eduardo/OneDrive/Trade_Edu/news.xlsx',header=0)
    #data['date'] = news['Date']
    #data['Score'] = news['compound_vader_score']
    #data['Manchete'] = news['title']

    connection = sqlite3.connect('noticias.db')
    noticiasValor = pd.read_sql('select * from noticias', connection)
    data['Manchete'] = noticiasValor['Manchetes Valor']

    connection = sqlite3.connect('noticiasCNBC.db')
    noticiasCNBC = pd.read_sql('select * from noticiasCNBC', connection)
    data['MancheteCNBC'] = noticiasCNBC['Manchetes CNBC']


    return render(request, 'contas/news.html', data)

@login_required(login_url='/login/')
def posicaoBBAS(request):
    data = {}
    posicaoBBAS = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Relatorio_InvestSystem.xlsx",sheet_name='Posicao_BBAS3',header=0)

    posicaoBBAS['Descobertas'] = round(posicaoBBAS['Descobertas'], 2)
    posicaoBBAS['Descobertas.1'] = round(posicaoBBAS['Descobertas.1'], 2)

    ###Coleta dados de Call##
    data['codigo'] = posicaoBBAS['Código']
    data['strike'] = posicaoBBAS['Strike']
    data['descoberta'] = posicaoBBAS['Descobertas']
    data['titulares'] = posicaoBBAS['Titulares']
    data['lancadores'] = posicaoBBAS['Lançadores']
    ###Coleta dados de Put##
    data['codigoP'] = posicaoBBAS['Código.1']
    data['strikeP'] = posicaoBBAS['Strike.1']
    data['descobertaP'] = posicaoBBAS['Descobertas.1']
    data['titularesP'] = posicaoBBAS['Titulares.1']
    data['lancadoresP'] = posicaoBBAS['Lançadores.1']

    return render(request, 'contas/posicaobbas.html', data)

@login_required(login_url='/login/')
def rolagens(request):
    data = {}

    rolagem = pd.read_excel('InvestSystem3.0_django.xlsm', sheet_name='Robo_Rolagens',header=7)
      
    data['OpcaoC'] = rolagem['Opcao (C)']
    data['TipoC'] = rolagem['Tipo (C)']
    data['VencC'] = rolagem['Venc. (C)']
    data['StrikeC'] = rolagem['Strike (C)']
    data['CotacaoC'] = rolagem['Cotacao (C)']

    data['OpcaoV'] = rolagem['Opcao (V)']
    data['TipoV'] = rolagem['Tipo (V)']
    data['VencV'] = rolagem['Venc. (V)']
    data['StrikeV'] = rolagem['Strike (V)']
    data['CotacaoV'] = rolagem['Cotacao (V)']

    data['Spread'] = round(rolagem['Spread'],2)
    data['Sinal'] = rolagem['Sinal']
    data['Liquidez'] = rolagem['Liquidez']

    return render(request, 'contas/rolagens.html', data)

@login_required(login_url='/login/')
def painel(request):
    data = {}
    dados = pd.read_excel('InvestSystem3.0_django.xlsm', sheet_name='Banco_IBOV', keep_default_na='False', header=0)
    data['Nome'] = dados['Nome']
    data['Ativo'] = dados['Ativo']
    data['Cotacao'] = pd.to_numeric(dados['Cotacao'], errors='coerce')
    data['Variacao'] = round(dados['Variacao']*100,2)
    data['Maximo'] = round(dados['Maximo'],2)
    data['Minimo'] = round(dados['Minimo'],2)
    data['Volume'] = round(dados['Liquidez'])

    return render(request, 'contas/painel.html', data)

@login_required(login_url='/login/')
def fundamentos(request):
    data = {}
    fund = pd.read_excel('InvestSystem3.0_django.xlsm', sheet_name='Analise Fundament.', header=6)
    data['Empresa'] = fund['Empresa']
    data['Cotacao'] = fund['Cotacao']
    data['PrecoVPA'] = fund['.Preço/VPA']
    data['Dividendos'] = round(fund['.Dividend Yield']*100,2)
    data['VPA'] = fund['.VPA']
    data['LucroAcao'] = fund['.Lucro/Ação']
    data['Graham'] = round(fund['byGrahan'],2)

    return render(request, 'contas/fundamentos.html', data)

@login_required(login_url='/login/')
def posicaoPETR(request):
    data = {}
    posicaoBBAS = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Relatorio_InvestSystem.xlsx",sheet_name='Posicao_PETR4',header=0)

    posicaoBBAS['Descobertas'] = round(posicaoBBAS['Descobertas'], 2)
    posicaoBBAS['Descobertas.1'] = round(posicaoBBAS['Descobertas.1'], 2)

    ###Coleta dados de Call##
    data['codigo'] = posicaoBBAS['Código']
    data['strike'] = posicaoBBAS['Strike']
    data['descoberta'] = posicaoBBAS['Descobertas']
    data['titulares'] = posicaoBBAS['Titulares']
    data['lancadores'] = posicaoBBAS['Lançadores']
    ###Coleta dados de Put##
    data['codigoP'] = posicaoBBAS['Código.1']
    data['strikeP'] = posicaoBBAS['Strike.1']
    data['descobertaP'] = posicaoBBAS['Descobertas.1']
    data['titularesP'] = posicaoBBAS['Titulares.1']
    data['lancadoresP'] = posicaoBBAS['Lançadores.1']

    return render(request, 'contas/posicaopetr4.html', data)

@login_required(login_url='/login/')
def posicaoITUB(request):
    data = {}
    posicaoBBAS = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Relatorio_InvestSystem.xlsx",sheet_name='Posicao_ITUB4',header=0)

    posicaoBBAS['Descobertas'] = round(posicaoBBAS['Descobertas'], 2)
    posicaoBBAS['Descobertas.1'] = round(posicaoBBAS['Descobertas.1'], 2)

    ###Coleta dados de Call##
    data['codigo'] = posicaoBBAS['Código']
    data['strike'] = posicaoBBAS['Strike']
    data['descoberta'] = posicaoBBAS['Descobertas']
    data['titulares'] = posicaoBBAS['Titulares']
    data['lancadores'] = posicaoBBAS['Lançadores']
    ###Coleta dados de Put##
    data['codigoP'] = posicaoBBAS['Código.1']
    data['strikeP'] = posicaoBBAS['Strike.1']
    data['descobertaP'] = posicaoBBAS['Descobertas.1']
    data['titularesP'] = posicaoBBAS['Titulares.1']
    data['lancadoresP'] = posicaoBBAS['Lançadores.1']

    return render(request, 'contas/posicaoitub4.html', data)

@login_required(login_url='/login/')
def posicaoBBDC(request):
    data = {}
    posicaoBBAS = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Relatorio_InvestSystem.xlsx",sheet_name='Posicao_BBDC4',header=0)

    posicaoBBAS['Descobertas'] = round(posicaoBBAS['Descobertas'], 2)
    posicaoBBAS['Descobertas.1'] = round(posicaoBBAS['Descobertas.1'], 2)

    ###Coleta dados de Call##
    data['codigo'] = posicaoBBAS['Código']
    data['strike'] = posicaoBBAS['Strike']
    data['descoberta'] = posicaoBBAS['Descobertas']
    data['titulares'] = posicaoBBAS['Titulares']
    data['lancadores'] = posicaoBBAS['Lançadores']
    ###Coleta dados de Put##
    data['codigoP'] = posicaoBBAS['Código.1']
    data['strikeP'] = posicaoBBAS['Strike.1']
    data['descobertaP'] = posicaoBBAS['Descobertas.1']
    data['titularesP'] = posicaoBBAS['Titulares.1']
    data['lancadoresP'] = posicaoBBAS['Lançadores.1']

    return render(request, 'contas/posicaobbdc4.html', data)

@login_required(login_url='/login/')
def mapaPETR(request):
    data = {}
    mapaPETR = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Projeto_django/Robo_PUT_PETR4.xlsx",header=0)

    data['STRIKE'] = mapaPETR['STRIKE']
    data['ATIVO'] = mapaPETR['ATIVO']
    data['VENCIMENTO'] = mapaPETR['VENC.']
    data['SINAL'] = mapaPETR['Robo PUT']
    data['COTACAO'] = mapaPETR['Real Time']
    data['Tretorno'] = round(mapaPETR['TIR (%)']*100,4)
    data['PROTECAO'] = round(mapaPETR['Strike VS Cot. (%)']*100,2)
    data['ProbExerc'] = mapaPETR['Prob. Exec.']
    data['Negocios'] = mapaPETR['Negocios']
    return render(request, 'contas/mapapetr4.html', data)

@login_required(login_url='/login/')
def mapaITUB(request):
    data = {}
    mapaITUB = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Projeto_django/Robo_PUT_ITUB4.xlsx",header=0)

    data['STRIKE'] = mapaITUB['STRIKE']
    data['ATIVO'] = mapaITUB['ATIVO']
    data['VENCIMENTO'] = mapaITUB['VENC.']
    data['SINAL'] = mapaITUB['Robo PUT']
    data['COTACAO'] = mapaITUB['Real Time']
    data['Tretorno'] = round(mapaITUB['TIR (%)']*100,4)
    data['PROTECAO'] = round(mapaITUB['Strike VS Cot. (%)']*100,2)
    data['ProbExerc'] = mapaITUB['Prob. Exec.']
    data['Negocios'] = mapaITUB['Negocios']
    return render(request, 'contas/mapaitub4.html', data)

@login_required(login_url='/login/')
def index(request):
    data = {}
    return render(request, 'contas/index.html', data)

def home1(request):
    data = {}

    broad = pd.read_excel('C:/Users/Eduardo/OneDrive/Trade_Edu/BD_noticias.xlsx',sheet_name='broad',header=0)

    data['news'] = broad['Manchete']

    return render(request, 'contas/home1.html', data)

@login_required(login_url='/login/')
def dividendos(request):
    data = {}

    tabela = pd.read_excel('C:/Users/Eduardo/OneDrive/Trade_Edu/dividendos.xlsx')

    data['Empresa'] = tabela['Empresa']
    data['Tipo'] = tabela['Tipo']
    data['DataEx'] = tabela['DataEx']
    data['PrevPag'] = tabela['PrevPag']
    data['Valor'] = tabela['Valor']


    return render(request, 'contas/dividendos.html', data)

@login_required(login_url='/login/')
def carteira(request):
    data = {}
    return render(request, 'contas/carteira.html', data)