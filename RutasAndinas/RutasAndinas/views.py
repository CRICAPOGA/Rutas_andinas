from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from Sales.models import Sale
from Users.utils import role_required
from Plans.models import Plan

# Create your views here.
def home(request):
    return render(request, 'index.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def financial_view(request):
    sales = Sale.objects.all().order_by('-sale_date') #Organizar por fecha descendente
    total_earnings = sales.aggregate(total=Sum('total_cost'))['total'] or 0  # Suma total de ventas
    
    context = {
        'sales' : sales,
        'total_earnings' : total_earnings
    }

    return render(request, 'finances.html', context)

#Gestionar CrudPlan
@role_required('Empleado')
def plan_list_view(request):
    plans = Plan.objects.all()
    return render(request, 'CrudPlan/list.html', {'plans': plans})

#Catalogo de planes
@role_required('Turista')
def catalog_view(request):
    plans = Plan.objects.all()
    return render(request, 'Catalog/catalog.html', {'plans': plans})

#Detalle del plan
@role_required('Turista')
def plan_detail_view(request, plan_id):
    plan = get_object_or_404(Plan, plan_id=plan_id)
    return render(request, 'Catalog/detailsPlan.html', {'plan': plan})
