from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
import uuid
import pandas as pd

class Categoria(models.Model):
      #id = models.UUIDField( primary_key = False, default = uuid.uuid4().int, editable = False)
      nome = models.CharField(max_length=100)
      dt_criacao = models.DateTimeField(auto_now_add=True)

class Transacao(models.Model):
      data = models.DateTimeField()
      descricao = models.CharField(max_length=200)
      valor = models.DecimalField(max_digits=7, decimal_places=2)
      categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
      observacoes = models.TextField(null=True, blank=True)

class Trade(models.Model):

      STATUS = (
            ('doing', 'Doing'),
            ('done', 'Done'),
      )

      title = models.CharField(max_length=255)
      description = models.TextField()
      done = models.CharField(
            max_length=5,
            choices = STATUS,
      )

      user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      def __str__(self):
            return self.title

class Evolucao(models.Model):
      data = models.DateTimeField()
      valor = models.DecimalField(max_digits=7, decimal_places=2)

#Create your models here.
