from django.contrib import admin
from .models import Categoria
from .models import Transacao
from .models import Trade


admin.site.register(Categoria)
admin.site.register(Transacao)
admin.site.register(Trade)