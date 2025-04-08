from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from Users.models import Role, User

# Create your views here.
@staff_member_required(login_url='/')
@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

@staff_member_required(login_url='/')
@login_required
def crear_usuario(request):
    roles = Role.objects.all()
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
            usuario = User.objects.create_user(
                username=username, email=email, name=name,
                last_name=last_name, password=password, role_id=role
            )
            usuario.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect("lista_usuarios")
    
    return render(request, "crear_usuario.html", {"roles": roles})

@staff_member_required(login_url='/')
@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    roles = Role.objects.all()
    
    if request.method == "POST":
        usuario.username = request.POST["username"]
        usuario.email = request.POST["email"]
        usuario.name = request.POST["name"]
        usuario.last_name = request.POST["last_name"]
        role_id = request.POST["role_id"]
        usuario.role_id = get_object_or_404(Role, pk=role_id)
        
        if "password" in request.POST and request.POST["password"]:
            usuario.set_password(request.POST["password"])
        
        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("lista_usuarios")
    
    return render(request, "editar_usuario.html", {"usuario": usuario, "roles": roles})

@staff_member_required(login_url='/')
@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("lista_usuarios")