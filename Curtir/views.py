from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from RegistrarUsuarios.models import RegisterUser
from Timeline.models import Postagem
from Curtir.models import CurtirPostagem
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def curtir_postagem(request):
    usuario = request.user
    postagem_id = request.data.get('postagem_id')  
    if not postagem_id:
        return Response({
            "sucesso": False,
            "mensagem": "O ID da postagem é obrigatório.",
            "detalhes": None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        postagem = Postagem.objects.get(id=postagem_id)
        if CurtirPostagem.objects.filter(usuario=usuario, postagem=postagem).exists():
            return Response({
                "sucesso": False,
                "mensagem": "Você já curtiu essa postagem.",
                "detalhes": {
                    "usuario": usuario.apelido_usuario,
                    "postagem_id": postagem.id,
                    "postagem_titulo": postagem.titulo
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        CurtirPostagem.objects.create(usuario=usuario, postagem=postagem)
        return Response({
            "sucesso": True,
            "mensagem": "Curtida registrada com sucesso!",
            "detalhes": {
                "usuario": usuario.apelido_usuario,
                "postagem_id": postagem.id,
                "postagem_titulo": postagem.titulo,
                "autor_postagem": postagem.autor.apelido_usuario,
                "curtido_em": postagem.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            }
        }, status=status.HTTP_200_OK)
    except Postagem.DoesNotExist:
        return Response({
            "sucesso": False,
            "mensagem": "Postagem não encontrada.",
            "detalhes": None
        }, status=status.HTTP_404_NOT_FOUND)