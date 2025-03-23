from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, label="Nombre")
    last_name = forms.CharField(max_length=100, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo Electrónico")
    ROLES = forms.ChoiceField(choices=[("admin", "Admin"), ("empleado", "Empleado"), ("turista", "Turista")], label="Rol")
    
    class Meta:
        model = Usuario
        fields = ["username", "email", "password1", "password2", "last_name", "ROLES"]

class EditarUsuarioForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol']