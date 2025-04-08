from django.shortcuts import render, redirect, get_object_or_404
from Plans.models import Plan, Category, Plan_date, Picture
from Reviews.models import Review
from django.contrib import messages
from django.utils.timezone import now
import os
from django.db.models import Avg
from django.contrib.auth.decorators import login_required, user_passes_test

def is_employee(user):
    return (user.role_id and user.role_id.role == "Empleado") or user.is_staff

############## CRUD PLANS ##############

@login_required
@user_passes_test(is_employee) 
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

@login_required 
@user_passes_test(is_employee) 
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

@login_required
@user_passes_test(is_employee)
def viewPlan(request, plan_id):
    # Obtener el plan por su ID
    plan = get_object_or_404(Plan, plan_id=plan_id)
    # Obtener imágenes y fechas asociadas al plan
    pictures = Picture.objects.filter(plan_id=plan)
    plan_dates = Plan_date.objects.filter(plan_id=plan)
    # Mostrar
    return render(request, 'CrudPlan/viewPlan.html', {
        'plan': plan,
        'pictures': pictures,
        'plan_dates': plan_dates
    })

@login_required 
@user_passes_test(is_employee)
def editPlan(request, plan_id):
    # Obtener plan, categorías, imagenes y fechas asociadas al plan
    plan = get_object_or_404(Plan, plan_id=plan_id)
    categories = Category.objects.all() 
    existing_pictures = Picture.objects.filter(plan_id=plan)
    existing_dates = Plan_date.objects.filter(plan_id=plan).values_list('plan_date', flat=True)

    if request.method == 'POST':
        # Obtener los datos enviados a través del formulario
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '').strip()
        places = request.POST.get('places', '').strip()
        has_transport = request.POST.get('has_transport') == 'on'
        has_meal = request.POST.get('has_meal') == 'on'
        has_guide = request.POST.get('has_guide') == 'on'
        category_id = request.POST.get('category')
        plan_dates = request.POST.getlist('plan_dates')
        images = request.FILES.getlist('pictures')
        delete_pictures = request.POST.getlist('delete_pictures')  # Imágenes a eliminar

        # Validaciones
        if not name:
            messages.error(request, 'El nombre del plan es obligatorio.')
        if not plan_dates:
            messages.error(request, 'Debe seleccionar al menos una fecha para el plan.')
        if not places.isdigit() or int(places) <= 0:
            messages.error(request, 'El número de cupos disponibles debe ser mayor que 0.')
        if category_id:
            selected_category = get_object_or_404(Category, category_id=category_id)
        else:
            messages.error(request, 'Debe seleccionar una categoría.')
        # Verificar si alguna fecha seleccionada es anterior al día actual
        today = now().date()
        for date in plan_dates:
            if date < today.strftime('%Y-%m-%d'):
                messages.error(request, f'La fecha {date} no puede ser anterior a hoy.')
        # Si hay errores de validación, vuelve a renderizar la página con los mensajes de error
        if messages.get_messages(request):
            return render(request, 'CrudPlan/editPlan.html', {
                'plan': plan, 
                'categories': categories, 
                'existing_pictures': existing_pictures, 
                'existing_dates': existing_dates})

        try:
            # Actualizar los datos del plan
            plan.name = name
            plan.description = description
            plan.price = price
            plan.places = int(places)
            plan.has_transport = has_transport
            plan.has_meal = has_meal
            plan.has_guide = has_guide
            plan.category_id = selected_category
            plan.save()

            # Comparar las fechas existentes con las nuevas
            new_dates = set(plan_dates)
            old_dates = set(existing_dates)
            # Obtener fechas nuevas o que se van a eliminar
            dates_to_add = new_dates - old_dates
            dates_to_remove = old_dates - new_dates
            # Eliminar las fechas 
            for date in dates_to_remove:
                Plan_date.objects.filter(plan_id=plan, plan_date=date).delete()
            # Agregar las fechas nuevas
            for date in dates_to_add:
                Plan_date.objects.create(plan_id=plan, plan_date=date)

            # Eliminar imágenes seleccionadas por el usuario
            if delete_pictures:
                for picture_id in delete_pictures:
                    try:
                        picture = Picture.objects.get(picture_id=picture_id)
                        image_path = picture.picture.path  # Ruta del archivo
                        picture.delete() # Eliminar la imagen de la base de datos
                        os.remove(image_path) # Eliminar el archivo de la carpeta media
                    except Picture.DoesNotExist:
                        messages.error(request, f'No se encontró la imagen con ID {picture_id}.')
                    except Exception as e:
                        messages.error(request, f'Error al eliminar la imagen: {str(e)}')

            # Verificar si quedan imágenes después de eliminar
            remaining_pictures = Picture.objects.filter(plan_id=plan)

            # Si no hay imágenes y no se han subido nuevas, mostrar un error
            if not remaining_pictures.exists() and not images:
                messages.error(request, 'Debe subir al menos una imagen para el plan.')
            
            # Mostrar mensaje de error
            if messages.get_messages(request):
                return render(request, 'CrudPlan/editPlan.html', {
                    'plan': plan, 
                    'categories': categories, 
                    'existing_pictures': existing_pictures, 
                    'existing_dates': existing_dates
                })

            # Subir nuevas imágenes sin borrar las existentes
            for image in images:
                Picture.objects.create(plan_id=plan, picture=image)
            
            # Verificar si hay imágenes después de agregar las nuevas
            if not Picture.objects.filter(plan_id=plan).exists():
                messages.error(request, 'Debe subir al menos una imagen para el plan.')
            # Mostrar mensaje de error
            if messages.get_messages(request):
                return render(request, 'CrudPlan/editPlan.html', {
                    'plan': plan, 
                    'categories': categories, 
                    'existing_pictures': existing_pictures, 
                    'existing_dates': existing_dates
                })
             # Si no hubo errores, mostrar mensaje de éxito
            messages.success(request, f'El plan "{plan.name}" ha sido actualizado exitosamente.')
            return redirect('list')
        except Exception as e:
            messages.error(request, f'Error al actualizar el plan: {str(e)}')

    return render(request, 'CrudPlan/editPlan.html', {
        'plan': plan, 
        'categories': categories, 
        'existing_pictures': existing_pictures, 
        'existing_dates': existing_dates
    })

@login_required
@user_passes_test(is_employee)
def deletePlan(request, plan_id):
    plan = get_object_or_404(Plan, plan_id=plan_id)
    
    if request.method == "POST":
        try:
            # Eliminar imágenes asociadas
            pictures = Picture.objects.filter(plan_id=plan)
            for picture in pictures:
                if picture.picture:  
                    image_path = picture.picture.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                picture.delete()

            # Eliminar fechas asociadas
            Plan_date.objects.filter(plan_id=plan).delete()

            # Eliminar el plan
            plan.delete()
            messages.success(request, f'El plan "{plan.name}" ha sido eliminado exitosamente.')
            return redirect('list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el plan: {str(e)}')

    return render(request, 'CrudPlan/deletePlan.html', {'plan': plan})

############## CATALOG ##############
def catalog(request):
    category_id = request.GET.get('category_id')  # Obtener el filtro de la URL
    avg_rating = request.GET.get('avg_rating') # Obtener el filtro de promedio de calificación de la URL
    categories = Category.objects.all() # Obtener todas las categorías
    # Filtrar los planes
    if category_id:
        plans = Plan.objects.filter(category_id=category_id, places__gt=0)
    else:
        plans = Plan.objects.filter(places__gt=0)

    # Obtener los planes recientes (últimos 5) y sus imágenes si tienen cupos
    recent_plans = Plan.objects.filter(places__gt=0).order_by('-plan_id')[:5]
    for plan in recent_plans:
        plan.pictures = Picture.objects.filter(plan_id=plan)
    
    # Obtener el promedio de calificación para cada plan
    plans_with_avg = []
    for plan in plans:
        avg = Review.objects.filter(plan_id=plan.plan_id).aggregate(Avg('rate'))['rate__avg'] or 0
        rounded_avg = round(avg, 1)

    # Filtrar según el promedio de calificación
        if avg_rating and rounded_avg < float(avg_rating):
            continue
        plans_with_avg.append({'plan': plan, 'avg_rating': rounded_avg})
        
    return render(request, 'Catalog/catalog.html', {
        'plans_with_avg': plans_with_avg,
        'categories': categories,
        'recent_plans': recent_plans,
    })

@login_required
def detailsPlan(request, plan_id):
    # Obtener el plan por su ID
    plan = get_object_or_404(Plan, plan_id=plan_id)
    # Verificar si el plan tiene cupos
    if plan.places <= 0:
        messages.error(request, "Este plan no está disponible.")
        return redirect('catalog')
    # Obtener imágenes y fechas asociadas al plan
    pictures = Picture.objects.filter(plan_id=plan)
    plan_dates = Plan_date.objects.filter(plan_id=plan)
    reviews = Review.objects.filter(plan_id=plan)
    # Mostrar
    return render(request, 'Catalog/detailsPlan.html', {
        'plan': plan,
        'pictures': pictures,
        'plan_dates': plan_dates,
        'reviews': reviews
    })