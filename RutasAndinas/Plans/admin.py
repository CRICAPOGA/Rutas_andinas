from django.contrib import admin
from .models import Categories, Plans, Pictures

# Register your models here.
admin.site.register(Categories)
admin.site.register(Plans)
admin.site.register(Pictures)