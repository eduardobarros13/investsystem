from django.db import models

class Categoria(models.Model):
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
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      def __str__(self):
            return self.title

#Create your models here.
