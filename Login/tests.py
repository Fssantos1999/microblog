from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase

class TestLogout(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testeuser@example.com',
            password='senha123',
            data_nascimento=date(1990, 1, 1) 
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)  
        self.access_token = str(refresh.access_token) 
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
    def test_logout(self):
        response = self.client.post('/api/v1/auth/logout/')  

        print(response.status_code)  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['message'], f"Logout realizado com sucesso! Usuário {self.user.email} desconectado.")
