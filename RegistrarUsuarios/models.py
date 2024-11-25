from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from datetime import date

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo de email é obrigatório")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)  # Usuário ativo por padrão
        usuario = self.model(email=email, **extra_fields)
        if password:
            usuario.set_password(password)  # Criptografa a senha
        else:
            raise ValueError("Senha obrigatória!")
        usuario.save(using=self._db)
        return usuario
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not password:
            raise ValueError("Superusuários devem ter uma senha.")
        return self.create_user(email, password, **extra_fields)


class RegisterUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=250, blank=False, null=False)
    telefone = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=250, unique=True, blank=False, null=False)
    apelido_usuario = models.CharField(max_length=15, null=True, blank=True, unique=True)
    data_nascimento = models.DateField(blank=False, null=False)
    usuario_ativo = models.BooleanField(default=True)
    administrador = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)  

    REQUIRED_FIELDS = ['nome', 'telefone', 'data_nascimento']
    USERNAME_FIELD = 'email'

    objects = UsuarioManager()

    def __str__(self):
        return self.email
    def ValidaMaiordeIdade(self):
        dia_atual = date.today()
        idade = dia_atual.year - self.data_nascimento.year - (
            (dia_atual.month, dia_atual.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
        if idade < 18:
            raise ValidationError("A idade mínima para o cadastro é de 18 anos.")
    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff
    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff
