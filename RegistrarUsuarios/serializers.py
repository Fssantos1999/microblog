from rest_framework import serializers
from .models import RegisterUser
import re

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Apenas para escrita
        required=True,  # Torna o campo obrigatório
        style={'input_type': 'password'}  # Para interfaces, exibe como senha
    )

    class Meta:
        model = RegisterUser
        fields = ['nome', 'telefone', 'email', 'data_nascimento', 'password', 'apelido_usuario']

    def validaSenha(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("A senha deve conter pelo menos um caractere especial.")
        
        return value

    def Cria_usuario_Com_Senha_Criptografada (self, validated_data):
        password = validated_data.pop('password')  
        user = RegisterUser(**validated_data)     
        user.set_password(password)               
        user.save()                               
        return user
