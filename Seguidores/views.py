from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Seguidor
from RegistrarUsuarios.models import RegisterUser

@api_view(['POST'])
def seguir_usuario(request, usuario_id):
    try:
        usuario = RegisterUser.objects.get(id=usuario_id)
        seguidor = request.user  # O usuário logado

        # Impedir que o usuário se siga
        if seguidor == usuario:
            return Response({"mensagem": "Você não pode seguir a si mesmo!"}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o seguidor já segue o usuário
        if Seguidor.objects.filter(usuario=usuario, seguidor=seguidor).exists():
            return Response({"mensagem": "Você já segue este usuário!"}, status=status.HTTP_400_BAD_REQUEST)

        # Cria a relação de seguidor
        Seguidor.objects.create(usuario=usuario, seguidor=seguidor)
        return Response({"mensagem": "Você agora segue este usuário!"}, status=status.HTTP_201_CREATED)
    except RegisterUser.DoesNotExist:
        return Response({"mensagem": "Usuário não encontrado!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def desseguir_usuario(request, usuario_id):
    try:
        usuario = RegisterUser.objects.get(id=usuario_id)
        seguidor = request.user  # O usuário logado

        # Verifica se a relação de seguimento existe
        seguimento = Seguidor.objects.filter(usuario=usuario, seguidor=seguidor)
        if not seguimento.exists():
            return Response({"mensagem": "Você não segue este usuário!"}, status=status.HTTP_400_BAD_REQUEST)

        # Remove a relação de seguimento
        seguimento.delete()
        return Response({"mensagem": "Você deixou de seguir este usuário!"}, status=status.HTTP_200_OK)
    except RegisterUser.DoesNotExist:
        return Response({"mensagem": "Usuário não encontrado!"}, status=status.HTTP_404_NOT_FOUND)
