from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from Timeline.models import Postagem
from .models import ComentarPostagem

User = get_user_model()

class ComentarPostagemTests(TestCase):

    def setUp(self):
        """
        Configuração dos dados para os testes. 
        - Criação de dois usuários (usuário comum e admin).
        - Criação de uma postagem para o comentário.
        """
        # Criação de usuários
        self.usuario_comum = User.objects.create_user(
            email="usuario@exemplo.com", password="senha123", nome="Usuário Comum"
        )
        self.usuario_admin = User.objects.create_user(
            email="admin@exemplo.com", password="senha123", nome="Admin", is_staff=True
        )
        
        # Criação de uma postagem
        self.postagem = Postagem.objects.create(
            titulo="Título da Postagem",
            conteudo="Conteúdo da postagem.",
            autor=self.usuario_admin
        )
        
        # URL base para comentário
        self.url_comentarios = reverse('criar_comentario')

    def test_criar_comentario(self):
        """
        Testa a criação de um comentário com sucesso.
        """
        # Criação de um comentário com o usuário comum
        self.client.login(email="usuario@exemplo.com", password="senha123")
        
        data = {
            'postagem': self.postagem.id,
            'conteudo': 'Este é um comentário.'
        }
        response = self.client.post(self.url_comentarios, data, format='json')
        
        # Verifica se o comentário foi criado com sucesso
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ComentarPostagem.objects.count(), 1)
        self.assertEqual(ComentarPostagem.objects.first().conteudo, 'Este é um comentário.')

    def test_editar_comentario_permissoes(self):
        """
        Testa se o autor do comentário ou o autor da postagem podem editar o comentário.
        """
        # Criação do comentário com o usuário comum
        self.client.login(email="usuario@exemplo.com", password="senha123")
        comentario = ComentarPostagem.objects.create(
            postagem=self.postagem,
            autor=self.usuario_comum,
            conteudo='Comentário inicial'
        )

        # O usuário comum tenta editar seu próprio comentário
        data = {'conteudo': 'Comentário editado pelo autor.'}
        url_editar = reverse('editar_comentario', kwargs={'pk': comentario.id})
        response = self.client.put(url_editar, data, format='json')
        
        # Verifica se o comentário foi editado com sucesso
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comentario.refresh_from_db()
        self.assertEqual(comentario.conteudo, 'Comentário editado pelo autor.')

        # O usuário admin tenta editar o comentário
        self.client.login(email="admin@exemplo.com", password="senha123")
        response = self.client.put(url_editar, data, format='json')
        
        # Verifica se o admin também pode editar
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Outro usuário tenta editar o comentário
        self.client.login(email="outro@exemplo.com", password="senha123")
        response = self.client.put(url_editar, data, format='json')
        
        # Verifica se um usuário sem permissão recebe erro de permissão
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remover_comentario_permissoes(self):
        """
        Testa se o autor do comentário ou o autor da postagem podem remover o comentário.
        """
        # Criação do comentário com o usuário comum
        self.client.login(email="usuario@exemplo.com", password="senha123")
        comentario = ComentarPostagem.objects.create(
            postagem=self.postagem,
            autor=self.usuario_comum,
            conteudo='Comentário a ser removido'
        )

        # O usuário comum tenta remover seu próprio comentário
        url_remover = reverse('remover_comentario', kwargs={'pk': comentario.id})
        response = self.client.delete(url_remover)
        
        # Verifica se o comentário foi removido com sucesso
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ComentarPostagem.objects.count(), 0)

        # O usuário admin tenta remover o comentário
        self.client.login(email="admin@exemplo.com", password="senha123")
        comentario = ComentarPostagem.objects.create(
            postagem=self.postagem,
            autor=self.usuario_comum,
            conteudo='Outro comentário a ser removido'
        )
        response = self.client.delete(url_remover)
        
        # Verifica se o admin também pode remover
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Outro usuário tenta remover o comentário
        self.client.login(email="outro@exemplo.com", password="senha123")
        response = self.client.delete(url_remover)
        
        # Verifica se um usuário sem permissão recebe erro de permissão
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

