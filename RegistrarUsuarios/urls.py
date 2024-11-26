from django.urls import path
from .views import register_user, delete_user, update_user, list_user, get_user_id

urlpatterns = [
    path('register/', register_user, name='register'),  
    path('delete/<int:user_id>/', delete_user, name='delete_user'),  # Alterado para usar ID
    path('update/<int:user_id>/', update_user, name='update_user'),  # Alterado para usar ID
    path('list/', list_user, name='list_user'),
    path('get-id/', get_user_id, name='get_id_user'),
]
