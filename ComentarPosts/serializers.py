from rest_framework import serializers
from .models import ComentarPostagem

class ComentarPostagemSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source="autor.nome", read_only=True)
    postagem_titulo = serializers.CharField(source="postagem.titulo", read_only=True)

    class Meta:
        model = ComentarPostagem
        fields = ['id', 'postagem_titulo', 'autor_nome', 'comentario', 'criado_em']
        extra_kwargs = {
            'comentario': {'source': 'conteudo'}  
        }
