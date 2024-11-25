from django.db import models
from django.core.exceptions import ValidationError

class CurtirPostagem(models.Model):
    usuario = models.ForeignKey(
        'RegistrarUsuarios.RegisterUser',  # Nome correto do modelo de usuário
        related_name='curtidas',
        on_delete=models.CASCADE  # Comportamento ao excluir o usuário
    )
    postagem = models.ForeignKey(
        'Timeline.Postagem',  # Nome correto do modelo de postagem (ajuste conforme o nome do app)
        related_name='curtidas',
        on_delete=models.CASCADE  # Comportamento ao excluir a postagem
    )
    curtido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'postagem'],
                name='usuario_postagem_unico'  # Garantir que cada usuário possa curtir uma postagem apenas uma vez
            )
        ]
        verbose_name = "Curtir postagem"
        verbose_name_plural = "Curtidas nas postagens"

    def __str__(self):
        return f"{self.usuario} curtiu a postagem '{self.postagem.titulo}'"

    def clean(self):
        if self.usuario == self.postagem.autor:
            raise ValidationError("Você não pode curtir sua própria postagem.")
