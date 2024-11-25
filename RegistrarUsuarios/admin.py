from django.contrib import admin
from .models import RegisterUser

class RegisterUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone', 'data_nascimento', 'usuario_ativo', 'administrador')
    list_filter = ('usuario_ativo', 'administrador')
    search_fields = ('nome', 'email', 'telefone')
    list_editable = ('usuario_ativo', 'administrador')
    ordering = ('nome',)

admin.site.register(RegisterUser, RegisterUserAdmin)
