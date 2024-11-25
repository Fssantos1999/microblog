from django.db import models
from RegistrarUsuarios.models import RegisterUser
from Timeline.models import Postagem

class Feed(models.Model):
    usuario = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='feeds')
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='feeds')  # Associação com Postagem
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feed de {self.usuario.apelido_usuario} - Postagem: {self.postagem.titulo}"
