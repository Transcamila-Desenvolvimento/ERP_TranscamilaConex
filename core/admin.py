from django.contrib import admin
from .models import Filial, Ambiente, UsuarioFilial, SessaoUsuario

@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'cidade', 'ativa']
    list_filter = ['ativa', 'cidade']
    search_fields = ['codigo', 'nome', 'cidade']

@admin.register(Ambiente)
class AmbienteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'app_name', 'url_name', 'ativo']
    list_filter = ['ativo']
    search_fields = ['codigo', 'nome', 'app_name']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'nome', 'ativo', 'descricao')
        }),
        ('Configuração de Acesso', {
            'fields': ('app_name', 'url_name'),
            'description': 'Configuração para vincular este ambiente a um app Django específico'
        }),
    )

@admin.register(UsuarioFilial)
class UsuarioFilialAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'filial', 'get_ambientes']
    list_filter = ['filial', 'ambientes']
    filter_horizontal = ['ambientes']
    
    def get_ambientes(self, obj):
        return ", ".join([str(ambiente) for ambiente in obj.ambientes.all()])
    get_ambientes.short_description = 'Ambientes'

@admin.register(SessaoUsuario)
class SessaoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'ultimo_ambiente', 'ultima_filial', 'em_selecao_ambiente', 'ultima_url', 'data_ultima_atividade']
    readonly_fields = ['data_ultima_atividade']
    list_filter = ['em_selecao_ambiente']
    search_fields = ['usuario__username', 'ultima_url']