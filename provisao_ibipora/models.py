from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class ContaFixa(models.Model):
    # Filial (ex: PORTO ALEGRE)
    filial = models.CharField(
        max_length=50,
        verbose_name="Filial",
        help_text="Nome da filial (ex: PORTO ALEGRE)"
    )

    # Produto (código longo, como 5053000020)
    produto = models.CharField(
        max_length=20,
        verbose_name="Produto",
        help_text="Código do produto (ex: 5053000020)"
    )

    # Código (ex: FS0920)
    codigo = models.CharField(
        max_length=10,
        verbose_name="Cód.",
        help_text="Código curto da conta (ex: FS0920)"
    )

    # Centro de Custo
    centro_custo = models.CharField(
        max_length=10,
        verbose_name="C. Custo",
        help_text="Código do centro de custo (ex: 2512001)"
    )

    # Tipo de Documento (NFS, NF, etc.)
    TIPO_DOCUMENTO_CHOICES = [
        ('NFS', 'NFS'),
        ('NF', 'NF'),
        ('BOLETO', 'Boleto'),
        ('OUTROS', 'Outros'),
    ]
    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='NFS',
        verbose_name="Doc.",
        help_text="Tipo de documento"
    )

    # Drive (ex: MUNICIPAL, ESTADUAL)
    drive = models.CharField(
        max_length=20,
        verbose_name="Drive",
        help_text="Origem ou tipo de envio (ex: MUNICIPAL)"
    )

    # Fornecedor
    fornecedor = models.CharField(
        max_length=100,
        verbose_name="Fornecedor",
        help_text="Nome do fornecedor ou razão social"
    )

    # Valor
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor",
        help_text="Valor da conta fixa"
    )

    # Grupo (ex: 000004)
    grupo = models.CharField(
        max_length=10,
        verbose_name="Grupo",
        help_text="Código do grupo"
    )

    # Chegada (ex: "Todo dia 5")
    chegada = models.CharField(
        max_length=50,
        verbose_name="Chegada",
        help_text="Regra de vencimento (ex: Todo dia 5, Dia 10, etc.)"
    )

    # Observações
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações",
        help_text="Observações adicionais (ex: quem envia, responsável)"
    )

    # Segmento (ex: Assessoria, Manutenção, etc.)
    segmento = models.CharField(
        max_length=50,
        verbose_name="Segmento",
        help_text="Categoria da conta (ex: Assessoria, Aluguel)"
    )

    # Data de cadastro (opcional, para histórico)
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    # Atualizado em
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Conta Fixa"
        verbose_name_plural = "Contas Fixas"
        ordering = ['filial', 'chegada', 'fornecedor']
        indexes = [
            models.Index(fields=['filial']),
            models.Index(fields=['chegada']),
            models.Index(fields=['segmento']),
        ]

    def __str__(self):
        return f"{self.filial} - {self.fornecedor} - R$ {self.valor}"

    # Método auxiliar para formatar valor como no template
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_formatado.short_description = "Valor"


    