from django.urls import path
from . import views
from .views import employee_plan_list, tourist_catalog, tourist_details

urlpatterns = [
    path('', views.plan, name='list'),
    path('create/', views.createPlan, name='createPlan'),
    path('view/<int:plan_id>/', views.viewPlan, name='viewPlan'),
    path('edit/<int:plan_id>/', views.editPlan, name='editPlan'),
    path('delete/<int:plan_id>/', views.deletePlan, name='deletePlan'),
    
    path('catalog/', views.catalog, name='catalog'),
    path('details/<int:plan_id>/', views.detailsPlan, name='detailsPlan'),
    
    path('employee/plans/', employee_plan_list, name='employee_plan_list'),
    path('catalog/', tourist_catalog, name='tourist_catalog'),
    path('catalog/<int:plan_id>/', tourist_details, name='tourist_details'),
]