from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Review
from Plans.models import Plan
from Users.models import User

# Crear una reseña
def create_review(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)

    if request.method == "POST":
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
    return redirect("detailsPlan", plan_id=plan_id)
