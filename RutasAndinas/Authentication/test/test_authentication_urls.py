from django.urls import resolve
from Authentication.views import login_view, login_auth, logout_view, register_view
from django.contrib.auth import views as auth_views

def test_url_login():
    resolver = resolve("/authentication/login/")
    assert resolver.func == login_view

def test_url_login_auth():
    resolver = resolve("/authentication/login_auth/")
    assert resolver.func == login_auth

def test_url_logout():
    resolver = resolve("/authentication/logout/")
    assert resolver.func == logout_view

def test_url_register():
    resolver = resolve("/authentication/register/")
    assert resolver.func == register_view
