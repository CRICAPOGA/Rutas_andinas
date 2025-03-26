from django.db import models
from Plans.models import Plan_date
from Users.models import User

# Create your models here.
class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True, verbose_name="Id")
    plan_date_id = models.ForeignKey(Plan_date, on_delete=models.CASCADE, verbose_name='Plan')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    total_cost = models.IntegerField(verbose_name="Total Cost")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Sale date")

    def __str__(self):
        return str(self.user_id.name) + ' - ' + str(self.date)