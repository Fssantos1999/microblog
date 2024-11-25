from django.db import models
from RegistrarUsuarios.models import RegisterUser  # Importando o modelo de usuário

# Modelo de Seguidores
class Seguidor(models.Model):
    usuario = models.ForeignKey(
        RegisterUser,  # Usuário sendo seguido
        on_delete=models.CASCADE,
        related_name='seguindo',  # Nome reverso para quem está seguindo
    )
    
    seguidor = models.ForeignKey(
        RegisterUser,  # Usuário que está seguindo
        on_delete=models.CASCADE,
        related_name='seguidores',  # Nome reverso para os seguidores
    )

    class Meta:
        unique_together = ('usuario', 'seguidor')  # Impede que o mesmo seguidor siga o mesmo usuário mais de uma vez
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'

    def __str__(self):
        return f"{self.seguidor.apelido_usuario} segue {self.usuario.apelido_usuario}"
