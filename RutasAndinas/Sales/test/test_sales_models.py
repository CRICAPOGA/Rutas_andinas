from django.test import TestCase
from Plans.models import Category, Plan, Plan_date
from Users.models import User
from Sales.models import Sale
from datetime import date

class Sale_model_test(TestCase):
    def setUp(self):
        """Configura una categoría, un plan, una fecha de plan y un usuario para usar en los tests"""
        self.category = Category.objects.create(category="Aventura")
        self.plan = Plan.objects.create(
            category_id=self.category,
            name="Escapada a la playa",
            description="Un plan de aventura en la playa.",
            price=150000,
            places=20,
            has_transport=True,
            has_meal=False,
            has_guide=True
        )
        self.plan_date = Plan_date.objects.create(
            plan_id=self.plan,
            plan_date=date(2025, 5, 1)
        )
        self.user = User.objects.create(
            name="Juan Perez",
            email="juan.perez@example.com",
            username="juanperez",
            password="password123"
        )

    def test_create_sale(self):
        """Prueba la creación de una venta"""
        sale = Sale.objects.create(
            plan_date_id=self.plan_date,
            user_id=self.user,
            total_cost=300000,
            number_of_people=2,
            payment_method="Tarjeta",
        )
        
        # Recuperamos la venta de la base de datos
        saved_sale = Sale.objects.get(sale_id=sale.sale_id)

        # Verificamos los valores
        self.assertEqual(saved_sale.plan_date_id.plan_id.name, 'Escapada a la playa')
        self.assertEqual(saved_sale.plan_date_id.plan_date, date(2025, 5, 1))
        self.assertEqual(saved_sale.user_id.name, 'Juan Perez')
        self.assertEqual(saved_sale.total_cost, 300000)
        self.assertEqual(saved_sale.number_of_people, 2)
        self.assertEqual(saved_sale.payment_method, 'Tarjeta')
        self.assertEqual(saved_sale.sale_date.strftime('%d/%m/%Y'), sale.sale_date.strftime('%d/%m/%Y'))

    def test_sale_str_method(self):
        """Prueba el método __str__ del modelo Sale"""
        sale = Sale.objects.create(
            plan_date_id=self.plan_date,
            user_id=self.user,
            total_cost=300000,
            number_of_people=2,
            payment_method="Tarjeta",
        )
        
        # Verificamos que el método __str__ funcione correctamente
        self.assertEqual(str(sale), f"{self.user.name} - {sale.sale_date.strftime('%d/%m/%Y')}")
