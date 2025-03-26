from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True, verbose_name="Id")
    category = models.CharField(max_length=30, verbose_name="Category")

    def __str__(self):
        return self.category
    
class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True, verbose_name="Id")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    name = models.CharField(max_length=30, verbose_name="Name")
    description = models.CharField(max_length=1000, verbose_name="Description")
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Price")
    places = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Places")
    has_transport = models.BooleanField(default=False, verbose_name="Has Transport?")
    has_meal = models.BooleanField(default=False, verbose_name="Has Meal?")
    has_guide = models.BooleanField(default=False, verbose_name="Has Guide?")

    def __str__(self):
        return self.name

class Plan_date(models.Model):
    plan_date_id = models.AutoField(primary_key=True, verbose_name="Id")
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name="Plan")
    plan_date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

class Picture(models.Model):
    picture_id = models.AutoField(primary_key=True, verbose_name="Id")
    picture = models.ImageField(upload_to="galery/", null=False, blank=False, default=None)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='Plans')

    def __str__(self):
        return str(self.picture_id) + '-' + self.plan_id.name