from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Feed, Postagem
from .serializers import FeedSerializer
from Seguidores.models import Seguidor
from .serializers import PostagemSerializer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_feed(request):
    usuario = request.user

    # Obter IDs dos usuários seguidos
    seguidos_ids = Seguidor.objects.filter(seguidor=usuario).values_list('usuario_id', flat=True)

    # Adicionar o próprio usuário ao feed
    seguidos_ids = list(seguidos_ids) + [usuario.id]

    # Recuperar as postagens dos usuários seguidos e do próprio usuário
    postagens = Postagem.objects.filter(autor_id__in=seguidos_ids).order_by('-criado_em')

    # Serializar as postagens
    serializer = PostagemSerializer(postagens, many=True)

    # Verificar se há postagens no feed
    if not postagens.exists():
        return Response({
            "sucesso": True,
            "mensagem": f"Bem-vindo ao feed, {usuario.apelido_usuario}! Parece que ainda não há postagens no seu feed.",
            "postagens": []
        }, status=status.HTTP_200_OK)

    # Responder com as postagens disponíveis
    return Response({
        "sucesso": True,
        "mensagem": f"Bem-vindo ao feed, {usuario.apelido_usuario}! Aqui estão as suas postagens e as das pessoas que você segue.",
        "postagens": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def favoritar_feed(request, feed_id):
    try:
        feed = Feed.objects.get(id=feed_id)
    except Feed.DoesNotExist:
        return Response(
            {"mensagem": "Feed não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    if feed.favorita:
        return Response(
            {"mensagem": "A postagem já está favoritada."},
            status=status.HTTP_400_BAD_REQUEST
        )
    feed.favoritar()

    return Response(
        {"mensagem": "Favoritado com sucesso.", "favorita": feed.favorita},
        status=status.HTTP_200_OK
    )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def desfavoritar_feed(request, feed_id):
    try:
        feed = Feed.objects.get(id=feed_id)
    except Feed.DoesNotExist:
        return Response(
            {"mensagem": "Feed não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    if not feed.favorita:
        return Response(
            {"mensagem": "A postagem não está favoritada."},
            status=status.HTTP_400_BAD_REQUEST
        )
    feed.desfavoritar()
    return Response(
        {"mensagem": "Desfavoritado com sucesso.", "favorita": feed.favorita},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def alimentar_feed(request):
    try:
        usuario = request.user
        seguidores = Seguidor.objects.filter(usuario=usuario).values_list('seguidor', flat=True)
        if not seguidores:
            return Response({"mensagem": "Você não tem seguidores."}, status=status.HTTP_404_NOT_FOUND)
        postagens = Postagem.objects.filter(autor__in=seguidores)
        if not postagens:
            return Response({"mensagem": "Não há postagens para exibir."}, status=status.HTTP_404_NOT_FOUND)
        for postagem in postagens:
            Feed.objects.get_or_create(usuario=usuario, postagem=postagem)
        return Response({"mensagem": "Feed alimentado com sucesso."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"mensagem": f"Erro ao alimentar feed: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
