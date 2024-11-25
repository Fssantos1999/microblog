from django.urls import path
from . import views

urlpatterns = [
    path('postagens/', views.criar_postagem, name='criar_postagem'),  # POST para criar
    path('postagens/<int:id>/', views.detalhes_postagem, name='detalhes_postagem'),  # GET para detalhes
    path('postagens/<int:id>/update/', views.atualizar_postagem, name='atualizar_postagem'),  # PUT para atualizar
    path('postagens/<int:id>/delete/', views.deletar_postagem, name='deletar_postagem'),  # DELETE para excluir
]
                                                                                        