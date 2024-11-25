from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas da API
    path('api/v1/users/', include('RegistrarUsuarios.urls')),  
    path('api/v1/auth/', include('Login.urls')),  
    path('api/v1/', include('Timeline.urls')),  
    path('api/v1/', include('Seguidores.urls')),
    path('api/v1/', include('ComentarPosts.urls')),
    path('api/v1/', include('Curtir.urls')),
    path('api/v1/', include('Feed.urls')),

    # Rotas para a documentação com Swagger e Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Gera o schema da API
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # UI do Swagger
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # UI do Redoc (alternativa ao Swagger)
]
