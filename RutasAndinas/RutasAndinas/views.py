from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from Sales.models import Sale

# Create your views here.
def home(request):
    return render(request, 'index.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def financial_view(request):
    sales = Sale.objects.all().order_by('-sale_date') #Organizar por fecha descendente
    print(f"sales count: {sales.count()}")
    total_earnings = sales.aggregate(total=Sum('total_cost'))['total'] or 0  # Suma total de ventas
    
    context = {
        'sales' : sales,
        'total_earnings' : total_earnings
    }

    return render(request, 'finances.html', context)