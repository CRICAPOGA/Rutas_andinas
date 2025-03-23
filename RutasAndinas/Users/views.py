from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistroUsuarioForm, EditarUsuarioForm
from .models import Usuario

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios")  # Redirige a la lista de usuarios
    else:
        form = RegistroUsuarioForm()
    
    return render(request, "Users/registro.html", {"form": form})

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "users/lista.html", {"usuarios": usuarios})

def editar_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, "users/editar.html", {"form": form, "usuario": usuario})

def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('lista_usuarios')