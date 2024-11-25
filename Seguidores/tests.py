from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from RegistrarUsuarios.models import RegisterUser
from Seguidores.models import Seguidor

class SeguidorTestCase(APITestCase):

    def setUp(self):
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
        self.token = Token.objects.create(user=self.seguidor)
        self.url = reverse('seguir_usuario', kwargs={'usuario_id': self.usuario.id})

    def test_seguir_usuario(self):
        self.assertIsNotNone(self.token.key)
        response = self.client.post(
            self.url,
            {},
            HTTP_AUTHORIZATION='Token ' + self.token.key  
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Seguidor.objects.filter(seguidor=self.seguidor, usuario=self.usuario).exists())

    def test_seguir_usuario_duplicado(self):
        response = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seguir_usuario_auto(self):
        url = reverse('seguir_usuario', kwargs={'usuario_id': self.seguidor.id})
        response = self.client.post(url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
