from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Postagem(models.Model):
    titulo = models.CharField(max_length=200, blank=False)
    conteudo = models.TextField()
    autor = models.ForeignKey('RegistrarUsuarios.RegisterUser', related_name='postagens', on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    publicado_em = models.DateTimeField(null=True, blank=True)
    visualizacoes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    def clean(self):
        alerta = {}
        if len(self.conteudo) < 10:
            alerta['conteudo'] = "O conteúdo da postagem deve ter no mínimo 10 caracteres."
        if len(self.titulo) < 5:
            alerta['titulo'] = "O título da postagem deve ter no mínimo 5 caracteres."
        if alerta:
            raise ValidationError(alerta)

    @property
    def is_published(self):
        return bool(self.publicado_em)

    def save(self, *args, **kwargs):
        if not self.publicado_em:
            self.publicado_em = timezone.now()
        self.clean()

        super().save(*args, **kwargs)
