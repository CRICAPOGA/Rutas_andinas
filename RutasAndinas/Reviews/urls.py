from django.urls import path
from . import views
app_name = 'reviews'
urlpatterns = [
    path('<int:plan_id>/create/', views.create_review, name='create_review'),
    path('<int:plan_id>/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('<int:plan_id>/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]