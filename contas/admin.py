from django.contrib import admin
from .models import Categoria
from .models import Transacao
from .models import Trade
from .models import Evolucao


admin.site.register(Trade)
admin.site.register(Evolucao)
