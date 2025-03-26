from django.contrib import admin
from .models import Category, Plan, Plan_date, Picture

# Register your models here.
admin.site.register(Category)
admin.site.register(Plan)
admin.site.register(Plan_date)
admin.site.register(Picture)