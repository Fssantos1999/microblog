from django.urls import path
from . import views

urlpatterns = [
    path('comentarios/', views.criar_comentario, name='criar_comentario'),
    path('comentarios/<int:id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('comentarios/<int:id>/excluir/', views.excluir_comentario, name='excluir_comentario'),
    path('comentarios/<int:postagem_id>/', views.listar_comentarios, name='listar_comentarios'),
]
