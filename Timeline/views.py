from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Postagem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import PostagemSerializer
from Seguidores.models import Seguidor
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_postagem(request):
    if request.method == 'POST':
        serializer = PostagemSerializer(data=request.data)
        if serializer.is_valid():
            postagem = serializer.save(autor=request.user)
            return Response({
                "status": "sucesso",
                "mensagem": "Postagem criada com sucesso!",
                "data": {
                    "id": postagem.id,
                    "titulo": postagem.titulo,
                    "conteudo": postagem.conteudo,
                    "autor": {
                        "id": postagem.autor.id,
                        "apelido": postagem.autor.apelido_usuario,
                        "nome": postagem.autor.nome,
                        "email": postagem.autor.email
                    },
                    "criado_em": postagem.criado_em.isoformat(),
                    "atualizado_em": postagem.atualizado_em.isoformat(),
                    "visualizacoes": postagem.visualizacoes,
                    "publicado_em": postagem.publicado_em.isoformat() if postagem.publicado_em else None,
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "erro",
            "mensagem": "Ocorreu um problema ao criar a postagem.",
            "detalhes": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletar_postagem(request, id):
    try:
        postagem = get_object_or_404(Postagem, id=id)
        if postagem.autor != request.user:
            return Response({
                "status": "erro",
                "mensagem": "Você não tem permissão para excluir esta postagem."
            }, status=status.HTTP_403_FORBIDDEN)
        postagem.delete()  
        return Response({
            "status": "sucesso",
            "mensagem": "Postagem deletada com sucesso!"
        }, status=status.HTTP_204_NO_CONTENT)
    except Postagem.DoesNotExist:
        return Response({
            "status": "erro",
            "mensagem": "Postagem não encontrada."
        }, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def atualizar_postagem(request, id):
    try:
        postagem = get_object_or_404(Postagem, id=id)
        if postagem.autor != request.user:
            return Response({
                "status": "erro",
                "mensagem": "Você não tem permissão para atualizar esta postagem."
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = PostagemSerializer(postagem, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "sucesso",
                "mensagem": "Postagem atualizada com sucesso!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Postagem.DoesNotExist:
        return Response({
            "status": "erro",
            "mensagem": "Postagem não encontrada."
        }, status=status.HTTP_404_NOT_FOUND)
        
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalhes_postagem(request, id):
    try:
        postagem = get_object_or_404(Postagem, id=id)  
    except Postagem.DoesNotExist:
        return Response(
            {"status": "erro", "mensagem": "Postagem não encontrada."}, 
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PostagemSerializer(postagem)


    postagens_autor_count = Postagem.objects.filter(autor=postagem.autor).count()

   
    seguidores_count = Seguidor.objects.filter(seguidor=postagem.autor).count()  
    
    response_data = {
        "status": "sucesso",
        "mensagem": "Postagem encontrada com sucesso.",
        "data": {
            "id": postagem.id,
            "titulo": postagem.titulo,
            "conteudo": postagem.conteudo,
            "visualizacoes": postagem.visualizacoes,
            "autor": {
                "id": postagem.autor.id,
                "apelido": postagem.autor.apelido_usuario,
                "nome": postagem.autor.nome,
                "email": postagem.autor.email,
                "postagens": postagens_autor_count,
                "seguidores": seguidores_count,  
                "data_cadastro": postagem.autor.date_joined.isoformat(),
                "links": {
                    "perfil": f"https://api.exemplo.com/usuarios/{postagem.autor.id}/",
                    "postagens": f"https://api.exemplo.com/usuarios/{postagem.autor.id}/postagens/"
                }
            },
            "criado_em": postagem.criado_em.isoformat(),
            "atualizado_em": postagem.atualizado_em.isoformat(),
             "links": {
                "exibir_publicacão": f"http://localhost:8000/api/v1/postagens/{postagem.id}/", 
                "atualizar_publicacão": f"http://localhost:8000/api/v1/postagens/{postagem.id}/update/", 
                "deletar_publicacão": f"http://localhost:8000/api/v1/postagens/{postagem.id}/delete/",  
            }
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)