from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_usuarios, name='index_usuarios'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
]