from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Review
from Plans.models import Plan
from Sales.models import Sale
from Users.models import User
from django.contrib.auth.decorators import login_required

# Crear una reseña
@login_required
def create_review(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    current_user = request.user
    already_bought = Sale.objects.filter(user_id=current_user).exists()

    if request.method == "POST":
        if already_bought:
            content = request.POST.get("content")
            rate = int(request.POST.get("rate", 0))
            # Validar que el contenido y la calificación sean obligatorios
            if not content:
                messages.error(request, "El comentario no puede estar vacío.")
                return redirect("detailsPlan", plan_id=plan_id)
            
            if content and 0 <= rate <= 5:
                # Crear la reseña
                Review.objects.create(
                    content=content,
                    rate=rate,
                    plan_id=plan,
                    user_id=request.user
                )
                messages.success(request, "Reseña creada exitosamente.")
                return redirect("detailsPlan", plan_id=plan_id)
        else:
            messages.warning(request, 'Parece que aún no has adquirido este plan.¿Te gustaría hacerlo ahora?')
            return redirect("detailsPlan", plan_id=plan_id)

    return redirect("detailsPlan", plan_id=plan_id)

# Editar una reseña
@login_required
def edit_review(request, plan_id, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # Verificar que el usuario actual es el creador de la reseña
    if review.user_id != request.user:
        messages.error(request, "No tienes permiso para editar esta reseña.")
        return redirect("detailsPlan", plan_id=plan_id)

    if request.method == "POST":
        content = request.POST.get("content")
        rate = int(request.POST.get("rate", 0))

        # Validación
        if not content:
            messages.error(request, "El comentario no puede estar vacío.")
        elif not (0 <= rate <= 5):
            messages.error(request, "La calificación debe estar entre 0 y 5.")
        else:
            # Actualizar la reseña
            review.content = content
            review.rate = rate
            review.save()
            messages.success(request, "Reseña actualizada exitosamente.")
            return redirect("detailsPlan", plan_id=plan_id)

    return redirect("detailsPlan", plan_id=plan_id)

# Eliminar una reseña
@login_required
def delete_review(request, plan_id, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # Verificar que el usuario actual es el creador de la reseña
    if review.user_id != request.user:
        messages.error(request, "No tienes permiso para eliminar esta reseña.")
        return redirect("detailsPlan", plan_id=plan_id)

    # Eliminar la reseña
    review.delete()
    messages.success(request, "Reseña eliminada exitosamente.")
    return redirect("detailsPlan", plan_id=plan_id)
