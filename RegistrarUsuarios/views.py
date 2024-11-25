from rest_framework import status
from rest_framework.decorators import api_view, permission_classes  # Importe permission_classes corretamente
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import RegisterUser
from .serializers import RegisterUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404 
from django.contrib.auth.hashers import check_password as check_pass  # Importar a função correta
import re


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            # A senha é tratada e criptografada usando set_password
            password = request.data.get('password', '')
            if password:
                user = serializer.save()
                user.set_password(password)  # Criptografa a senha
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"mensagem": "Senha obrigatória!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
def delete_user(request, usuario_email):
    try:
        user = RegisterUser.objects.get(email=usuario_email)
    except RegisterUser.DoesNotExist:
        return Response(
            {"mensagem": "Usuário não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.user != user and not request.user.is_staff:
        return Response(
            {"mensagem": "Você não tem permissão para deletar este usuário."},
            status=status.HTTP_403_FORBIDDEN
        )
    if request.user == user and request.user.is_staff:
        return Response(
            {"mensagem": "Administradores não podem deletar sua própria conta."},
            status=status.HTTP_400_BAD_REQUEST
        )
    user.delete()
    return Response(
        {"mensagem": "Usuário deletado com sucesso."},
        status=status.HTTP_204_NO_CONTENT
    )



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, usuario_email):
    try:
        user = RegisterUser.objects.get(email=usuario_email)  
    except RegisterUser.DoesNotExist:
        return Response(
            {"Erro": "Usuário não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.user != user and not request.user.is_staff:
        return Response(
            {"Erro": "Você não tem permissão para atualizar este usuário."},
            status=status.HTTP_403_FORBIDDEN
        )
    serializer = RegisterUserSerializer(user, data=request.data, partial=True)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#Lista usuarios de 5 em 5 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user(request):
    list_users = RegisterUser.objects.all().order_by('nome')
    paginator = Paginator(list_users, 5)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except Exception:
        return Response({"mensagem": "Número da página inválido."}, status=status.HTTP_400_BAD_REQUEST)
    serializer = RegisterUserSerializer(page_obj, many=True)
    response_data = {
        "pagina_atual": page_obj.number,
        "total_paginas": paginator.num_pages,
        "total_usuarios": paginator.count,
        "usuarios": serializer.data,    
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_id(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response(
            {'mensagem':'favor inserir o id para que possa ser feito a request'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = RegisterUser.objects.get(id=user_id)
        return Response({
            'id': user.id,
            'apelido': user.apelido_usuario,
            'email': user.email
        })
    except RegisterUser.DoesNotExist:
        return Response({
            'mensagem: f"Usuario  com ID {user_id} não  localizado, favor verificar id ou usuario foi deletado"'
        })

