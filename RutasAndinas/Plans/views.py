from django.shortcuts import render
from Plans.models import Plan, Category, Plan_date

############## CRUD PLANS ##############

#@login_required 
def plan(request):
    category_id = request.GET.get('category_id')  # Obtener el filtro de la URL
    categories = Category.objects.all() # Obtener todas las categorías
    # Filtrar los planes
    if category_id:
        plans = Plan.objects.filter(category_id=category_id)
    else:
        plans = Plan.objects.all()
    # Agregar las fechas disponibles de cada plan
    for plan in plans:
        plan.dates_available = Plan_date.objects.filter(plan_id=plan)
        
    return render(request, 'CrudPlan/list.html', {'plans': plans, 'categories': categories})
