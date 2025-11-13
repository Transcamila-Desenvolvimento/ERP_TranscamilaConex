# admin.py
from django.contrib import admin
from .models import ContaFixa

@admin.register(ContaFixa)
class ContaFixaAdmin(admin.ModelAdmin):
    list_display = ('filial', 'produto', 'codigo', 'centro_custo', 'fornecedor', 'valor_formatado', 'chegada', 'segmento')
    list_filter = ('filial', 'segmento', 'chegada', 'tipo_documento')
    search_fields = ('filial', 'fornecedor', 'produto', 'codigo', 'observacoes')
    ordering = ('filial', 'chegada')