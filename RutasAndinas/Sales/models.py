from django.db import models
from Plans.models import Plans
from Users.models import Users

# Create your models here.
class Sales(models.Model):
    sale_id = models.AutoField(primary_key=True, verbose_name="Id")
    plan_id = models.ForeignKey(Plans, on_delete=models.CASCADE, verbose_name='Plan')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='User')
    total_cost = models.IntegerField(verbose_name="Total Cost")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    def __str__(self):
        return str(self.user_id.name) + ' - ' + str(self.date)