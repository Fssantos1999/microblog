from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model  
from django.contrib.auth.hashers import check_password as check_pass  # Função para verificar a senha
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes  # Importe permission_classes corretamente
from rest_framework_simplejwt.tokens import RefreshToken
import re

from rest_framework import status

User = get_user_model() 
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    senha = request.data.get("senha") 
    if not email or not senha:
        return Response({"Erro": "Email e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"Erro": "Email inválido."}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not check_pass(senha, user.password):  
        return Response({"Erro": "Senha inválida."}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    return Response({
        "access": access_token,
        "refresh": str(refresh),
    }, status=status.HTTP_200_OK)
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def change_password(request):
    senha_atual = request.data.get('senha_atual')
    nova_senha = request.data.get('nova_senha')
    if not senha_atual or not nova_senha:
        return Response(
            {"mensagem": "A senha atual e a nova senha são obrigatórias."},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = request.user
        if not user.check_password(senha_atual):
            return Response(
                {"mensagem": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(nova_senha) < 8: 
            return Response(
                {"mensagem": "A nova senha deve ter pelo menos 8 caracteres."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(nova_senha)
        user.save()
        return Response(
            {"mensagem": "Senha alterada com sucesso!"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"mensagem": f"Erro ao alterar a senha: {str(e)}. Tente novamente mais tarde."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def logout(request):
    refresh_token = request.data.get('refresh_token')
    
    if not refresh_token:
        return Response(
            {"mensagem": "O refresh_token é obrigatório para realizar o logout."},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  
        return Response(
            {"mensagem": "Esperamos te ver novamente, até mais!"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"mensagem": f"Ocorreu um problema ao desconectar: {str(e)}. Por favor, tente novamente mais tarde."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
