from django.db import models
from Plans.models import Plan_date
from Users.models import User

# Create your models here.
class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True, verbose_name="Id")
    plan_date_id = models.ForeignKey(Plan_date, on_delete=models.CASCADE, verbose_name='Plan')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    total_cost = models.IntegerField(verbose_name="Total Cost")
    number_of_people = models.IntegerField(default=1, verbose_name="Number of People")
    payment_method = models.CharField(max_length=50, default="Tarjeta", verbose_name="Payment Method")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Sale date")

    def __str__(self):
        return f"{self.user_id.name} - {self.sale_date.strftime('%d/%m/%Y')}"