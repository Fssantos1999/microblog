from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from RegistrarUsuarios.models import RegisterUser
from Seguidores.models import Seguidor

class SeguidorTestCase(APITestCase):

    def setUp(self):
        """
        Configura os usuários para os testes
        """
        # Criação de dois usuários para o teste
        self.usuario = RegisterUser.objects.create_user(
            email="usuario@teste.com",
            password="senha123",
            nome="Usuário Teste",
            telefone="123456789",
            data_nascimento="1990-01-01"
        )
        
        self.seguidor = RegisterUser.objects.create_user(
            email="seguidor@teste.com",
            password="senha123",
            nome="Seguidor Teste",
            telefone="987654321",
            data_nascimento="1995-01-01"
        )

        # Gera o token de autenticação para o seguidor
        self.token = Token.objects.create(user=self.seguidor)

        # A URL para a criação de um seguidor, passando o ID do usuário a ser seguido
        self.url = reverse('seguir_usuario', kwargs={'usuario_id': self.usuario.id})

    def test_seguir_usuario(self):
        """
        Teste de criação de seguidor.
        """
        # Verifique se o token foi gerado corretamente
        self.assertIsNotNone(self.token.key)

        # Autentica o seguidor usando o token
        response = self.client.post(
            self.url,
            {},
            HTTP_AUTHORIZATION='Token ' + self.token.key  # Passando o token no header corretamente
        )
        
        # Verifica se a resposta é um sucesso (status HTTP 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se o seguidor foi de fato criado
        self.assertTrue(Seguidor.objects.filter(seguidor=self.seguidor, usuario=self.usuario).exists())

    def test_seguir_usuario_duplicado(self):
        """
        Testa a tentativa de seguir o mesmo usuário mais de uma vez.
        """
        # Primeiro segue o usuário
        response = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Tenta seguir novamente (o seguidor não pode seguir o mesmo usuário duas vezes)
        response = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Verifica se a resposta é um erro (status HTTP 400 Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seguir_usuario_auto(self):
        """
        Testa a tentativa de seguir a si mesmo.
        """
        # URL para seguir a si mesmo (deve falhar)
        url = reverse('seguir_usuario', kwargs={'usuario_id': self.seguidor.id})

        response = self.client.post(url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Verifica se a resposta é um erro (status HTTP 400 Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
