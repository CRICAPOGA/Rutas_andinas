from django.urls import path
from . import views
app_name = 'sales'

urlpatterns = [
    path('create_sale/<int:plan_id>/', views.create_sale, name='create_sale'),
    path('receipt/<int:sale_id>/', views.receipt, name='receipt'),
    path('receipt/<int:sale_id>/pdf/', views.generate_pdf_receipt, name='generate_pdf_receipt')
]
