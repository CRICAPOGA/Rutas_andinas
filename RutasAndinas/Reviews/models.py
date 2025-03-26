from django.db import models
from django.core.validators import MinValueValidator
from Plans.models import Plans
from Users.models import Users

# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True, verbose_name="Id")
    content = models.CharField(max_length=1000, verbose_name="Review Content")
    rate = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Rate")
    plan_id = models.ForeignKey(Plans, on_delete=models.CASCADE, verbose_name='Plan')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return str(self.rate) + ' - ' + str(self.user_id.name)