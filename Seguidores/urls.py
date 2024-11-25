from django.urls import path
from . import views

urlpatterns = [
    path('seguir/<int:usuario_id>/', views.seguir_usuario, name='seguir_usuario'),
    path('desseguir/<int:usuario_id>/', views.desseguir_usuario, name='desseguir_usuario'),
]
