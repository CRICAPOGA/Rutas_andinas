import pytest
from django.urls import reverse
from Plans.models import Category, Plan, Plan_date, Picture
from Reviews.models import Review
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from Users.models import Role

User = get_user_model()
@pytest.fixture
def authenticated_client(client, db):
    # Crear rol Empleado
    role = Role.objects.create(role="Empleado")
    
    # Crear usuario con ese rol
    user = User.objects.create_user(
        username="empleado",
        password="password123",
        role_id=role
    )

    # Loguear al usuario
    client.login(username="empleado", password="password123")
    return client

@pytest.mark.django_db
def test_plan_view(authenticated_client):
    category = Category.objects.create(category="Aventura")
    plan = Plan.objects.create(
        category_id=category,
        name="Tour Montaña",
        description="Excursión a la montaña",
        price=100,
        places=10,
        has_transport=True,
        has_meal=True,
        has_guide=True
    )
    Plan_date.objects.create(plan_id=plan, plan_date=timezone.now().date())
    
    response = authenticated_client.get(reverse('list'))
    assert response.status_code == 200
    assert 'plans' in response.context
    assert 'categories' in response.context
    assert plan in response.context['plans']

@pytest.mark.django_db
def test_view_plan(authenticated_client):
    category = Category.objects.create(category="Playa")
    plan = Plan.objects.create(
        category_id=category,
        name="Tour Playa",
        description="Relax en la playa",
        price=150,
        places=20,
        has_transport=False,
        has_meal=True,
        has_guide=False
    )
    picture = Picture.objects.create(plan_id=plan, picture='galery/test.jpg')
    Plan_date.objects.create(plan_id=plan, plan_date=timezone.now().date())

    response = authenticated_client.get(reverse('viewPlan', kwargs={'plan_id': plan.plan_id}))
    assert response.status_code == 200
    assert response.context['plan'] == plan
    assert 'pictures' in response.context
    assert 'plan_dates' in response.context

@pytest.mark.django_db
def test_catalog_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(category="Cultura")
    plan1 = Plan.objects.create(
        category_id=category,
        name="Tour Ciudad",
        description="Visita guiada por la ciudad",
        price=80,
        places=15,
        has_transport=True,
        has_meal=False,
        has_guide=True
    )
    Review.objects.create(plan_id=plan1, rate=4, user_id=user)
    Review.objects.create(plan_id=plan1, rate=3, user_id=user)


    response = client.get(reverse('catalog'))
    assert response.status_code == 200
    assert 'plans_with_avg' in response.context
    assert 'recent_plans' in response.context
    assert any(p['plan'] == plan1 for p in response.context['plans_with_avg'])

@pytest.mark.django_db
def test_details_plan_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(category="Deportes")
    plan = Plan.objects.create(
        category_id=category,
        name="Tour Bicicleta",
        description="Paseo en bicicleta",
        price=50,
        places=12,
        has_transport=True,
        has_meal=False,
        has_guide=True
    )
    Plan_date.objects.create(plan_id=plan, plan_date=timezone.now().date())
    Review.objects.create(plan_id=plan, rate=4, user_id=user)

    response = client.get(reverse('detailsPlan', kwargs={'plan_id': plan.plan_id}))
    assert response.status_code == 200
    assert response.context['plan'] == plan
    assert 'pictures' in response.context
    assert 'plan_dates' in response.context
    assert 'reviews' in response.context
