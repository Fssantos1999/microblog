from django.urls import path
from .views import register_user, delete_user, update_user, list_user,get_user_id   

urlpatterns = [
    path('register/', register_user, name='register'),  
    path('delete/<str:user_email>/', delete_user, name='delete_user'),  
    path('update/<str:user_email>/', update_user, name='update_user'),
    path('list/', list_user, name='list_user'),
    path('getID/', get_user_id, name='get_id_user')

]
