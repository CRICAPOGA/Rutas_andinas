from django.shortcuts import render, get_object_or_404, redirect
from Plans.models import Plan, Plan_date
from .models import Sale
from django.contrib import messages
from datetime import datetime
import locale
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import tempfile
from django.contrib.auth.decorators import login_required

@login_required
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
            plan_date_id= Plan_date.objects.get(plan_id=plan_id, plan_date=selected_date),
            user_id=request.user,
            total_cost=total_price,
            number_of_people=num_people,
            payment_method=payment_method,
        )

        # Descontar los cupos del plan
        plan.places -= num_people
        plan.save()

        messages.success(request, f'Compra realizada exitosamente por un total de ${total_price}')
        return redirect('sales:receipt', sale_id=sale.sale_id)

    return render(request, 'create_sale.html', {
        'plan': plan,
        'plan_dates': plan_dates,
        'price_per_person': total_price_per_person,
        'total_price': total_price,
    })

@login_required
def receipt(request, sale_id):
    sale = get_object_or_404(Sale, sale_id=sale_id)

    # Generar los datos para el código QR (puedes personalizar esta parte)
    qr_data = f"Venta ID: {sale.sale_id}\nPlan: {sale.plan_date_id.plan_id.name}\nTotal: ${sale.total_cost}\nFecha: {sale.sale_date}"

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Crear la imagen del QR
    img = qr.make_image(fill='black', back_color='white')

    # Convertir la imagen a un formato adecuado para respuesta HTTP
    qr_image = BytesIO()
    img.save(qr_image)
    qr_image.seek(0)
    qr_image_base64 = base64.b64encode(qr_image.getvalue()).decode('utf-8')

    return render(request, 'receipt.html', {
        'sale': sale,
        'qr_image_base64': qr_image_base64
    })

@login_required
def generate_pdf_receipt(request, sale_id):
    sale = get_object_or_404(Sale, sale_id=sale_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recibo_{sale.sale_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # ======= Espacio en blanco arriba =======
    top_margin = 40  # Margen superior de 40 puntos
    y_start = height - top_margin  # Comenzamos más abajo

    # ======= Encabezado del negocio =======
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, y_start - 20, "Rutas Andinas S.A.S")
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, y_start - 35, "Calle Falsa 123 - Bogotá, Colombia")
    p.drawCentredString(width / 2, y_start - 50, "Tel: (601) 123 4567 | rutasandinas@empresa.com")

    # Línea divisoria
    p.setStrokeColor(colors.black)
    p.line(50, y_start - 60, width - 50, y_start - 60)

    # ======= Título del recibo =======
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, y_start - 80, "Recibo de Compra")

    # ======= Detalles del recibo en recuadro =======
    p.setFont("Helvetica", 12)
    p.rect(80, 530, 430, 100, stroke=1, fill=0)
    y = 610
    spacing = 15
    p.drawString(100, y, f"ID de Venta: {sale.sale_id}")
    p.drawString(100, y - spacing, f"Plan: {sale.plan_date_id.plan_id.name}")
    p.drawString(100, y - 2 * spacing, f"Total: ${sale.total_cost}")
    p.drawString(100, y - 3 * spacing, f"Método de Pago: {sale.payment_method}")
    p.drawString(100, y - 4 * spacing, f"Fecha de Compra: {sale.sale_date.strftime('%d/%m/%Y')}")

    # ======= Código QR =======
    qr_data = f"Venta ID: {sale.sale_id}\nPlan: {sale.plan_date_id.plan_id.name}\nTotal: ${sale.total_cost}\nFecha: {sale.sale_date}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color='black', back_color='white')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file_path = tmp_file.name
        qr_image.save(tmp_file_path)
        p.drawImage(tmp_file_path, 420, 400, width=100, height=100)

    # ======= Mensaje final =======
    p.setFont("Helvetica-Oblique", 11)
    p.drawCentredString(width / 2, 380, "¡Gracias por su compra!")

    p.showPage()
    p.save()

    return response
