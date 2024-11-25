from rest_framework import serializers
from .models import Postagem

class PostagemSerializer(serializers.ModelSerializer):
    apelido = serializers.CharField(source='autor.apelido_usuario', read_only=True)

    class Meta:
        model = Postagem
        fields = ['id', 'titulo', 'conteudo', 'apelido', 'criado_em', 'atualizado_em', 'visualizacoes']
        read_only_fields = ['criado_em', 'atualizado_em', 'visualizacoes']

    def validate_titulo(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("O título deve ter no mínimo 5 caracteres.")
        return value

    def validate_conteudo(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("O conteúdo deve ter no mínimo 10 caracteres.")
        return value
