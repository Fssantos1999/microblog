from rest_framework import serializers
from .models import Feed
from Timeline.serializers import PostagemSerializer 
from RegistrarUsuarios.serializers import RegisterUserSerializer  
class FeedSerializer(serializers.ModelSerializer):
    postagem_titulo = serializers.CharField(source='postagem.titulo')
    postagem_conteudo = serializers.CharField(source='postagem.conteudo')

    class Meta:
        model = Feed
        fields = ['usuario', 'postagem_titulo', 'postagem_conteudo', 'criado_em', 'atualizado_em']