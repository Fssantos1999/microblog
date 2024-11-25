from django.urls import path
from . import views

urlpatterns = [
    path('feeds/', views.listar_feed, name='feed_listar'),
    path('feeds/favoritar/<int:feed_id>/', views.favoritar_feed, name='feed_favoritar'),
    path('feeds/desfavoritar/<int:feed_id>/', views.desfavoritar_feed, name='feed_desfavoritar'),
    path('feeds/alimentar/', views.alimentar_feed, name='feed_alimentar'),
]
