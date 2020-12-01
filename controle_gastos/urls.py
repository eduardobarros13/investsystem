"""controle_gastos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
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
from contas.views import index
from contas.views import home1
from contas.views import academia
from contas.views import dividendos

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
    path('index/', index, name='url_index'),
    path('home1/', home1, name='url_home1'),
    path('academia/', views.academia, name='url_academia'),

    path('mapapetr4/', mapaPETR, name='url_mapapetr4'),
    path('dividendos/', dividendos, name='url_dividendos'),
    path('login/', login_user, name='url_login'),
    path('login/submit', submit_login, name='url_login'),
    path('logout/', logout_user),
   
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/submit', submit_login, name='url_login'),

]
