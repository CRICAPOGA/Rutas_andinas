from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Categories(models.Model):
    category_id = models.AutoField(primary_key=True, verbose_name="Id")
    category = models.CharField(max_length=30, verbose_name="Category")

    def __str__(self):
        return self.category
    
class Plans(models.Model):
    plan_id = models.AutoField(primary_key=True, verbose_name="Id")
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Category')
    name = models.CharField(max_length=30, verbose_name="Name")
    description = models.CharField(max_length=1000, verbose_name="Description")
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Price")
    hasTransport = models.BooleanField(default=False, verbose_name="Has Transport?")
    hasMeal = models.BooleanField(default=False, verbose_name="Has Meal?")
    hasGuide = models.BooleanField(default=False, verbose_name="Has Guide?")

    def __str__(self):
        return self.name
    
class Pictures(models.Model):
    picture_id = models.AutoField(primary_key=True, verbose_name="Id")
    picture = models.ImageField(upload_to="galery/", null=False, blank=False, default=None)
    plan_id = models.ForeignKey(Plans, on_delete=models.CASCADE, verbose_name='Plans')

    def __str__(self):
        return str(self.picture_id) + '-' + self.plan_id.name