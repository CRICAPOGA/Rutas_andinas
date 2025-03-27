from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan, name='list'),
    path('create/', views.createPlan, name='createPlan'),
]