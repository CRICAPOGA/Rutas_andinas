from django.shortcuts import render, redirect, get_object_or_404
from Plans.models import Plan, Category, Plan_date, Picture
from django.contrib import messages
from django.utils.timezone import now

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

#@login_required 
def createPlan(request):
    # Obtener todas las categorías
    category = Category.objects.all()
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.POST.get('name', '').strip() #Elimina espacios extra
        description = request.POST.get('description' ,'').strip()
        price = request.POST.get('price', '').strip()
        places = request.POST.get('places', '').strip()
        has_transport = request.POST.get('has_transport') == 'on'
        has_meal = request.POST.get('has_meal') == 'on'
        has_guide = request.POST.get('has_guide') == 'on'
        category_id = request.POST.get('category')
        plan_dates = request.POST.getlist('plan_dates')
        images = request.FILES.getlist('pictures')

        #Validaciones
        if not name:
            messages.error(request, 'El nombre del plan es obligatorio.')
            return render(request, 'CrudPlan/createPlan.html', {'categories': category})
        if not plan_dates:
            messages.error(request, 'Debe seleccionar al menos una fecha para el plan.')
            return render(request, 'CrudPlan/createPlan.html', {'categories': category})
        if not places.isdigit() or int(places)<=0:
            messages.error(request, 'El numero de cupos disponibles debe ser un número mayor que 0.')
            return render(request, 'CrudPlan/createPlan.html', {'categories': category})
        if not images:
            messages.error(request, 'Debe subir al menos una imagen para el plan.')
            return render(request, 'CrudPlan/createPlan.html', {'categories': category})
        if category_id:  # Verificamos que category_id no sea None o vacío
            selected_category = get_object_or_404(Category, category_id=category_id)  # Convertimos el ID en instancia
        else:
            messages.error(request, 'Debe seleccionar una categoría.')
            return render(request, 'CrudPlan/createPlan.html', {'categories': category})
        
        # Validar que todas las fechas sean futuras o actuales
        today = now().date()
        for date in plan_dates:
            if date < today.strftime('%Y-%m-%d'):
                messages.error(request, f'La fecha {date} no puede ser anterior a hoy.')
                return render(request, 'CrudPlan/createPlan.html', {'categories': category})
          
        try:
            # Crear el plan con los datos obtenidos
            plan = Plan.objects.create(
                name=name, 
                description = description, 
                price=price, 
                places=int(places),
                has_transport=has_transport,
                has_meal=has_meal,
                has_guide=has_guide,
                category_id=selected_category 
            )
            # Crear las fechas asociadas al plan
            for date in plan_dates:
                Plan_date.objects.create(plan_id=plan, plan_date=date)
            # Crear las imágenes asociadas al plan
            for image in images:
                Picture.objects.create(plan_id=plan, picture=image)
            
            # Mostrar mensaje de éxito
            messages.success(request, f'El plan "{plan.name}" ha sido creado exitosamente.')
            return redirect('list')
        except Exception as e:
            messages.error(request, f'Error al crear el plan: {str(e)}')
            return render(request, 'CrudPlan/createPlan.html', {'categories': category})
    return render(request, 'CrudPlan/createPlan.html', {'categories':category})
