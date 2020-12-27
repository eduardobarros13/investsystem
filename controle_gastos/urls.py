from django.contrib import admin
admin.autodiscover()
from django.urls import path
from contas.views import put
from contas.views import news
from contas.views import posicaoBBAS
from contas.views import posicaoPETR
from contas.views import posicaoITUB
from contas.views import posicaoBBDC

from contas.views import rolagens
from contas.views import painel
from contas.views import fundamentos
from contas.views import mapaPETR
from contas.views import mapaITUB
from contas.views import index
from contas.views import home1
from contas.views import academia
from contas.views import dividendos
from contas.views import carteira
from contas.views import diarioTrader
from contas.views import login_user
from contas.views import submit_login
from contas.views import logado
from contas.views import logout_user
from contas import views
from django.urls import path, include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('put/', put, name='url_roboput'),
    path('news/', news, name='url_news'),
    path('rolagens/', rolagens, name='url_rolagens'),
    path('painel/', painel, name='url_painel'),
    path('fundamentos/', fundamentos, name='url_fundamentos'),
    path('posicaobbas/', posicaoBBAS, name='url_posicaoBBAS'),
    path('posicaoitub4/', posicaoITUB, name='url_posicaoitub4'),
    path('posicaobbdc4/', posicaoBBDC, name='url_posicaobbdc4'),
    path('posicaopetr4/', posicaoPETR, name='url_posicaopetr4'),
    path('carteira/', carteira, name='url_carteira'),
    path('index/', index, name='url_index'),
    path('home1/', home1, name='url_home1'),
    path('', home1, name='url_home1'),
    path('academia/', views.academia, name='url_academia'),
    path('mapapetr4/', mapaPETR, name='url_mapapetr4'),
    path('mapaitub4/', mapaITUB, name='url_mapaitub4'),
    path('mapabbdc4/', views.mapaBBDC, name='url_mapabbdc4'),
    path('planos/', views.planos, name='url_planos'),
    path('teste/', views.teste, name='url_teste'),



    path('dividendos/', dividendos, name='url_dividendos'),

    ###Criando banco do usuario###
    path('diario',diarioTrader, name='diario'),
    path('diario/<int:id>',views.diarioTraderView, name='diario-view'),
    path('newTrade/',views.newTrade, name='newTrade'),
    path('edit/<int:id>',views.editTrade, name='edittrade'),
    path('changestatus/<int:id>',views.changestatus, name='changestatus'),
    path('delete/<int:id>',views.deleteTrade, name='delete-trade'),
    path('yourname/<str:name>', views.yourName, name='your-name'),

    ###Criando paginas de login###
    path('login/', login_user, name='url_login'),
    path('login/submit', submit_login, name='url_login'),
    path('logout/', logout_user),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/submit', submit_login, name='url_login'),

]
