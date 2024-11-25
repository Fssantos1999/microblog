from django.db import models
from RegistrarUsuarios.models import RegisterUser  # Importando o modelo de usuário
from Timeline.models import Postagem  # Importando o modelo de postagem

class ComentarPostagem(models.Model):
    postagem = models.ForeignKey(Postagem, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(RegisterUser, related_name='comentarios', on_delete=models.CASCADE)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comentário de {self.autor} na postagem {self.postagem.titulo}'
    
    class Meta:
        ordering = ['-criado_em']  # Ordenando os comentários por data de criação, do mais recente ao mais antigo
