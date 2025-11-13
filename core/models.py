from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Filial(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Ambiente(models.Model):
    codigo = models.IntegerField(unique=True)  # Código numérico
    nome = models.CharField(max_length=100)
    app_name = models.CharField(
        max_length=100, 
        null=True,  # Temporariamente permite nulo
        blank=True,
        help_text="Nome do app Django (ex: provisao_ibipora)"
    )
    url_name = models.CharField(
        max_length=100, 
        default='home',
        help_text="Nome da URL (ex: home)"
    )
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def get_absolute_url(self):
        """Retorna a URL absoluta para este ambiente"""
        if self.app_name:
            try:
                return reverse(f'{self.app_name}:{self.url_name}')
            except:
                return reverse('selecao_ambiente')
        return reverse('selecao_ambiente')

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class UsuarioFilial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    ambientes = models.ManyToManyField(Ambiente)

    class Meta:
        unique_together = ('usuario', 'filial')

    def __str__(self):
        return f"{self.usuario.username} - {self.filial.nome}"

class SessaoUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    ultimo_ambiente = models.ForeignKey(Ambiente, on_delete=models.SET_NULL, null=True, blank=True)
    ultima_filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True)
    ultima_url = models.CharField(max_length=500, blank=True, null=True)
    em_selecao_ambiente = models.BooleanField(default=True)
    data_ultima_atividade = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sessão - {self.usuario.username}"

    def get_redirect_url(self):
        """Retorna a URL para redirecionar o usuário"""
        if self.em_selecao_ambiente:
            return reverse('selecao_ambiente')
        elif self.ultima_url:
            return self.ultima_url
        elif self.ultimo_ambiente:
            try:
                return self.ultimo_ambiente.get_absolute_url()
            except:
                return reverse('selecao_ambiente')
        else:
            return reverse('selecao_ambiente')