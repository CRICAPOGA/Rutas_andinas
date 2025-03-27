from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan, name='list'),
    path('create/', views.createPlan, name='createPlan'),
    path('view/<int:plan_id>/', views.viewPlan, name='viewPlan'),
    path('edit/<int:plan_id>/', views.editPlan, name='editPlan'),
    path('delete/<int:plan_id>/', views.deletePlan, name='deletePlan'),

    path('catalog/', views.catalog, name='catalog'),
    path('details/<int:plan_id>/', views.detailsPlan, name='detailsPlan'),
]