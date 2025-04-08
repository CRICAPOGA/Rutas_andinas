import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from Plans.models import Plan, Category

@pytest.mark.django_db
def test_list_view(client):
    url = reverse('list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_plan_view_get(client):
    url = reverse('createPlan')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_plan_view_post(client):
    url = reverse('createPlan')
    data = {
        'nombre': 'Plan de prueba',
        'descripcion': 'Descripción de prueba',
        'precio': 1000
    }
    response = client.post(url, data)
    assert response.status_code in (200, 302)  # Puede redirigir si es exitoso


@pytest.mark.django_db
def test_catalog_view(client):
    url = reverse('catalog')
    response = client.get(url)
    assert response.status_code == 200
