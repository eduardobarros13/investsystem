
from django.shortcuts import render, redirect, get_object_or_404
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

from .models import Trade
from .forms import TradeForm

###############Criando telas de logins###################

@login_required(login_url='/login/')
def academia(request):
    data ={}
    return render(request, 'contas/academia.html', data)

    
def logout_user(request):
    logout(request)
    return redirect('/login/')

def planos(request):
    data={}
    return render(request,'contas/planos.html', data)


def logado(request):
    return render (request, 'logado.html')


def login_user(request):
    logout(request)
    return render(request,'login.html')

@csrf_protect 
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = username, password=password, email=email)
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

        data['VolImplicita'] = banco['Vol Implicita']
        data['Delta'] = banco['Delta']
        data['Theta'] = banco['Theta']
        data['Gamma'] = banco['Gamma']
        data['PJusto'] = banco['Pjusto']



        return render(request, 'contas/home.html', data)
    time.sleep(6*5)

@login_required(login_url='/login/')
def news(request):
    data={}
    
    news = pd.read_excel('C:/Users/Eduardo/OneDrive/Trade_Edu/Novo_BD/BD_noticias.xlsx',header=0, sheet_name='broad')
    cnbc = pd.read_excel('C:/Users/Eduardo/OneDrive/Trade_Edu/Novo_BD/BD_noticias.xlsx',header=0, sheet_name='cnbc')

    data['Manchete'] = news['Manchete']
    data['MancheteCNBC'] = cnbc['Manchete']

    #connection = sqlite3.connect('noticias.db')
    #noticiasValor = pd.read_sql('select * from noticias', connection)
    #data['Manchete'] = noticiasValor['Manchetes Valor']

    #connection = sqlite3.connect('noticiasCNBC.db')
    #noticiasCNBC = pd.read_sql('select * from noticiasCNBC', connection)
    #data['MancheteCNBC'] = noticiasCNBC['Manchetes CNBC']


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
    data['descobertaP'] = list(posicaoBBAS['Descobertas.1'])
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

@login_required
def mapaPETR(request):
    data = {}
    mapaPETR = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Novo_BD/Mapeamento_PUT_PETR4.xlsx",header=0)

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

@login_required
def mapaITUB(request):

    data = {}
    mapaITUB = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Novo_BD/Mapeamento_PUT_ITUB4.xlsx",header=0)

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

@login_required
def mapaBBDC(request):
    data = {}
    mapa = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Novo_BD/Mapeamento_PUT_BBDC4.xlsx",header=0)

    data['STRIKE'] = mapa['STRIKE']
    data['ATIVO'] = mapa['ATIVO']
    data['VENCIMENTO'] = mapa['VENC.']
    data['SINAL'] = mapa['Robo PUT']
    data['COTACAO'] = mapa['Real Time']
    data['Tretorno'] = round(mapa['TIR (%)']*100,4)
    data['PROTECAO'] = round(mapa['Strike VS Cot. (%)']*100,2)
    data['ProbExerc'] = mapa['Prob. Exec.']
    data['Negocios'] = mapa['Negocios']
    return render(request, 'contas/mapabbdc4.html', data)

@login_required
def index(request):
    data = {}
    return render(request, 'contas/index.html', data)

def home1(request):
    data = {}

    news = pd.read_excel('C:/Users/Eduardo/OneDrive/Trade_Edu/Novo_BD/BD_noticias.xlsx',header=0, sheet_name='broad')
    data['Manchete'] = news['Manchete']

    return render(request, 'contas/home1.html', data)

@login_required
def dividendos(request):
    data = {}

    tabela = pd.read_excel('C:/Users/Eduardo/OneDrive/Trade_Edu/Novo_BD/BD_dividendos.xlsx')

    data['Empresa'] = list(tabela['Empresa'])
    data['Tipo'] = tabela['Tipo']
    data['DataEx'] = tabela['DataEx']
    data['PrevPag'] = tabela['PrevPag']
    data['Valor'] = list(tabela['Valor'])
    data['Valor2'] = list(tabela['Valor2'])
    return render(request, 'contas/dividendos.html', data)


def blog(request):
    data = {}
    return render(request, 'contas/blog.html', data)

@login_required
def teste(request):
    data = {}
    posicaoBBAS = pd.read_excel("C:/Users/Eduardo/OneDrive/Trade_Edu/Relatorio_InvestSystem.xlsx",sheet_name='Posicao_PETR4',header=0)

    posicaoBBAS['Descobertas'] = round(posicaoBBAS['Descobertas'], 2)
    posicaoBBAS['Descobertas.1'] = round(posicaoBBAS['Descobertas.1'], 2)

    ###Coleta dados de Call##
    data['codigo'] = list(posicaoBBAS['Código'])
    data['strike'] = posicaoBBAS['Strike']
    data['descoberta'] = list(posicaoBBAS['Descobertas'])
    data['titulares'] = posicaoBBAS['Titulares']
    data['lancadores'] = posicaoBBAS['Lançadores']
    ###Coleta dados de Put##
    data['codigoP'] = posicaoBBAS['Código.1']
    data['strikeP'] = posicaoBBAS['Strike.1']
    data['descobertaP'] = list(posicaoBBAS['Descobertas.1'])
    data['titularesP'] = posicaoBBAS['Titulares.1']
    data['lancadoresP'] = posicaoBBAS['Lançadores.1']

    return render(request, 'contas/teste.html', data)

@login_required
def carteira(request):
    data = {}
    return render(request, 'contas/carteira.html', data)
    

##criando area de usuario##
@login_required
def diarioTrader(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')
    tradeDone = Trade.objects.filter(done='done', user=request.user).count()
    tradeDoing = Trade.objects.filter(done='doing', user=request.user).count()

    if search:
        trade = Trade.objects.filter(title__icontains=search, user=request.user)
    elif filter:
        trade = Trade.objects.filter(done=filter, user=request.user)
    else:
        trade = Trade.objects.all().order_by('-created_at').filter(user=request.user)

    return render(request, 'contas/list.html', {'trade': trade,'tradedone': tradeDone, 'tradedoing': tradeDoing })



@login_required
def diarioTraderView(request, id):
    trade = get_object_or_404(Trade, pk=id)
    return render(request, 'contas/task.html', {'trade':trade})

@login_required
def newTrade(request):

    if request.method == 'POST':
        form = TradeForm(request.POST)

        if form.is_valid():
            trade = form.save(commit=False)
            trade.done = 'doing'
            trade.user = request.user
            trade.save()
            return redirect('/diario')

    else:
        form = TradeForm()
        return render(request, 'contas/addtrade.html', {'form': form})
            
    form = TradeForm()
    return render(request, 'contas/addtrade.html', {'form': form})
    
@login_required
def editTrade(request, id):
    trade = get_object_or_404(Trade, pk=id)
    form = TradeForm(instance = trade)
    if (request.method == 'POST'):
        form = TradeForm(request.POST, instance=trade)

        if (form.is_valid()):
            
            trade.save()
            return redirect('diario')
        else:
            return render(request, 'contas/edittrade.html', {'form':form, 'trade':trade})
    else:
        return render(request, 'contas/edittrade.html', {'form':form, 'trade':trade})

@login_required
def deleteTrade(request, id):
    trade = get_object_or_404(Trade, pk=id)
    
    trade.delete()

    messages.info(request, 'Trade deletado com sucesso')
    return redirect('diario')

@login_required
def changestatus(request, id):
    trade = get_object_or_404(Trade, pk=id)

    if (trade.done == 'doing'):
        trade.done = 'done'
    else:
        trade.done = 'doing'
    trade.save()
    return redirect('/diario')

@login_required
def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name':name})
        


