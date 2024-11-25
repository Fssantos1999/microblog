from django.urls import path
from . import views

urlpatterns = [
    # Criar um novo comentário
    path('comentarios/', views.criar_comentario, name='criar_comentario'),

    # Editar um comentário específico
    path('comentarios/<int:id>/editar/', views.editar_comentario, name='editar_comentario'),

    # Excluir um comentário específico
    path('comentarios/<int:id>/excluir/', views.excluir_comentario, name='excluir_comentario'),

    # Listar comentários de uma postagem específica
    path('comentarios/postagem/<int:postagem_id>/', views.listar_comentarios, name='listar_comentarios'),
]
