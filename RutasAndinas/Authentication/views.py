from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Users.models import User, Role

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def login_auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['password']
        user = authenticate(request, username=username, password=contraseña)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            messages.error(request,'Credenciales incorrectas')
            return render(request, 'login.html')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'login.html')

def register_view(request):
    roles = Role.objects.all()
    
    if request.method == 'POST':
        name = request.POST['name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role_id = 1

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.name = name
        user.last_name = last_name
        user.role_id = Role.objects.get(role_id=role_id) if role_id else None
        user.save()
        
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('login')
    
    return render(request, 'register.html', {'roles': roles})