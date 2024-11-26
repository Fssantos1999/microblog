from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ComentarPostagem
from Timeline.models import Postagem
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from .serializers import ComentarPostagemSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editar_comentario(request, id):
    comentario = get_object_or_404(ComentarPostagem, id=id)
    if comentario.autor != request.user:
        return Response(
            {'mensagem': 'Você não tem permissão para editar este comentário.'},
            status=status.HTTP_403_FORBIDDEN
        )

    novo_conteudo = request.data.get('conteudo')
    if not novo_conteudo:
        return Response(
            {'mensagem': 'Conteúdo do comentário não pode ser vazio.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    comentario.conteudo = novo_conteudo
    comentario.save()
    return Response({
        'id': comentario.id,
        'conteudo': comentario.conteudo,
        'comentado_por': comentario.autor.apelido_usuario,
        'postagem': comentario.postagem.titulo,
        'criado_em': comentario.criado_em
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_comentario(request, id):
    comentario = get_object_or_404(ComentarPostagem, id=id)
    if comentario.autor == request.user or comentario.postagem.autor == request.user:
        comentario.delete()
        return Response({'mensagem': 'Comentário excluído com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'mensagem': 'Você não tem permissão para excluir este comentário.'},
        status=status.HTTP_403_FORBIDDEN
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_comentarios(request, postagem_id):
    try:
        postagem = get_object_or_404(Postagem, id=postagem_id)
    except Http404:
        return Response(
            {'mensagem': 'Postagem não encontrada.'},
            status=status.HTTP_404_NOT_FOUND
        )
    comentarios = ComentarPostagem.objects.filter(postagem=postagem).values(
        'id', 'conteudo', 'autor__apelido_usuario', 'criado_em'
    )
    if not comentarios:
        return Response(
            {'mensagem': 'Não há comentários nesta postagem.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(list(comentarios), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_comentarios(request, postagem_id):
    # Filtra os comentários pela postagem_id
    comentarios = ComentarPostagem.objects.filter(postagem_id=postagem_id)
    paginador = PageNumberPagination()
    paginador.page_size = 5
    paginador.page_size_query_param = 'tamanho_pagina'
    paginador.max_page_size = 20
    resultados_paginados = paginador.paginate_queryset(comentarios, request)
    serializer = ComentarPostagemSerializer(resultados_paginados, many=True)

    return paginador.get_paginated_response({
        "status": "sucesso",
        "total_itens": paginador.page.paginator.count,
        "total_paginas": paginador.page.paginator.num_pages,
        "pagina_atual": paginador.page.number,
        "possui_proxima": paginador.page.has_next(),
        "possui_anterior": paginador.page.has_previous(),
        "comentarios": serializer.data
    })