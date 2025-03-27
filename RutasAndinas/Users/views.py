from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import User, Role
from django.contrib import messages

def registrar_usuario(request):
    role = Role.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        role_id = request.POST["role_id"]
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        else:
            role = get_object_or_404(Role, pk=role_id)
            usuario = User.objects.create(
                username=username, email=email, name=name,
                last_name=last_name, password=password, role=role
            )
            usuario.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect("lista_usuarios")
    
def lista_usuarios(request):
    User = User.objects.all()

def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    Role = Role.objects.all()
    
    if request.method == "POST":
        usuario.username = request.POST["username"]
        usuario.email = request.POST["email"]
        usuario.name = request.POST["name"]
        usuario.last_name = request.POST["last_name"]
        role_id = request.POST["role_id"]
        
        if "password" in request.POST and request.POST["password"]:
            usuario.set_password(request.POST["password"])
        
        usuario.role = get_object_or_404(Role, pk=role_id)
        usuario.save()
        messages.success(request, "Usuario actualizado exitosamente.")
        return redirect("lista_usuarios")

def eliminar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('lista_usuarios')

def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect("home")
        else:
            messages.error(request, "Credenciales incorrectas.")
    return render(request, "CRUD_usuarios/login.html")

def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login")