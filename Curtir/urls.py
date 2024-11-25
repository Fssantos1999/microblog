from django.urls import path
from . import views

urlpatterns = [
   path('curtir_postagem/', views.curtir_postagem, name='curtir_postagem'),
]
