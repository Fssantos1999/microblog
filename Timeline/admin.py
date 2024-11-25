from django.contrib import admin
from .models import Postagem

# Configurando a interface admin para o modelo Postagem
@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'criado_em', 'publicado_em', 'visualizacoes', 'is_published')
    list_filter = ('publicado_em', 'criado_em', 'autor')
    search_fields = ('titulo', 'conteudo', 'autor__email')
    ordering = ('-criado_em',)
    fields = ('titulo', 'conteudo', 'autor', 'publicado_em', 'visualizacoes', 'criado_em', 'atualizado_em')
    readonly_fields = ('criado_em', 'atualizado_em', 'visualizacoes')

    # Método customizado para exibir se a postagem está publicada
    def is_published(self, obj):
        return obj.is_published
    is_published.boolean = True  # Exibe como um ícone de "check" ou "x"
    is_published.short_description = "Publicado?"  # Nome da coluna no admin

    # Tornar campos não editáveis dependendo do estado da postagem
    def get_readonly_fields(self, request, obj=None):
        # Se a postagem foi publicada, 'publicado_em' não deve ser editável
        if obj and obj.is_published:
            return self.readonly_fields + ('publicado_em',)
        return self.readonly_fields
