from django.urls import path
from . import views
app_name = 'sales'

urlpatterns = [
    path('create_sale/<int:plan_id>/', views.create_sale, name='create_sale')
]