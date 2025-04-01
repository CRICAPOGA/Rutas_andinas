from django.shortcuts import render, get_object_or_404, redirect
from Plans.models import Plan, Plan_date
from .models import Sale
from django.contrib import messages
from datetime import datetime
import locale

def create_sale(request, plan_id):
    plan = get_object_or_404(Plan, plan_id=plan_id)
    plan_dates = Plan_date.objects.filter(plan_id=plan)

    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Inicializar total_price
    total_price = 0
    # Calcular el precio por persona aplicando porcentajes
    price_per_person = plan.price
    total_price_per_person = price_per_person
    
    if request.method == 'POST':
        num_people = int(request.POST.get('num_people', 1))  # Número de personas
        payment_method = request.POST.get('payment_method')
        selected_date_str = request.POST.get('selected_date')
        include_transport = request.POST.get('include_transport') == 'on'
        include_meal = request.POST.get('include_meal') == 'on'
        include_guide = request.POST.get('include_guide') == 'on'

        # Calculamos los porcentajes si las opciones son seleccionadas
        if include_transport:
            total_price_per_person *=1.25  # +25%
        if include_meal:
            total_price_per_person *= 1.10  # +10%
        if include_guide:
            total_price_per_person *= 1.05  # +5%
            
        # Calculamos el precio total basado en el número de personas
        total_price = total_price_per_person * num_people

        # Verificar si hay suficientes cupos disponibles
        if plan.places < num_people:
            messages.error(request, 'No hay suficientes cupos disponibles para la cantidad de personas seleccionadas.')
            return redirect('sales:create_sale', plan_id=plan.plan_id)  # Redirigir a la página del plan

        # Convertir el string de la fecha seleccionada al formato adecuado
        try:
            selected_date = datetime.strptime(selected_date_str, "%d de %B de %Y").date()
        except ValueError:
            # Si hay un error, puedes manejarlo de manera adecuada (por ejemplo, mostrar un mensaje de error)
            selected_date = None

        # Crear la venta y guardar en la base de datos
        sale = Sale.objects.create(
            plan_date_id=Plan_date.objects.get(plan_date=selected_date),
            user_id=request.user,
            total_cost=total_price,
            number_of_people=num_people,
            payment_method=payment_method,
        )

        # Descontar los cupos del plan
        plan.places -= num_people
        plan.save()

        messages.success(request, f'Compra realizada exitosamente por un total de ${total_price}')
        return redirect('detailsPlan', plan_id=plan.plan_id)

    return render(request, 'create_sale.html', {
        'plan': plan,
        'plan_dates': plan_dates,
        'price_per_person': total_price_per_person,
        'total_price': total_price,
    })