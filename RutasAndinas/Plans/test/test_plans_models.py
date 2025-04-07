from django.test import TestCase
from Plans.models import Category, Plan, Plan_date
from datetime import date

class Category_model_test(TestCase):
    def test_create_category(self):
        """Prueba la creación de una categoría"""
        category = Category.objects.create(category="Turismo")
        
        # Recuperamos la categoría de la base de datos
        saved_category = Category.objects.get(category="Turismo")

        # Verificamos los valores
        self.assertEqual(saved_category.category, 'Turismo')

class Plan_model_test(TestCase):
    def setUp(self):
        """Configura una categoría para usar en los tests"""
        self.category = Category.objects.create(category="Aventura")

    def test_create_plan(self):
        """Prueba la creación de un plan"""
        plan = Plan.objects.create(
            category_id=self.category,
            name="Escapada a la playa",
            description="Un plan de aventura en la playa.",
            price=150000,
            places=20,
            has_transport=True,
            has_meal=False,
            has_guide=True
        )
        
        # Recuperamos el plan de la base de datos
        saved_plan = Plan.objects.get(name="Escapada a la playa")

        # Verificamos los valores
        self.assertEqual(saved_plan.name, 'Escapada a la playa')
        self.assertEqual(saved_plan.description, 'Un plan de aventura en la playa.')
        self.assertEqual(saved_plan.price, 150000)
        self.assertEqual(saved_plan.places, 20)
        self.assertEqual(saved_plan.has_transport, True)
        self.assertEqual(saved_plan.has_meal, False)
        self.assertEqual(saved_plan.has_guide, True)
        self.assertEqual(saved_plan.category_id.category, 'Aventura')

class Plan_date_model_test(TestCase):
    def setUp(self):
        """Configura una categoría y un plan para usar en los tests"""
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

    def test_create_plan_date(self):
        """Prueba la creación de una fecha para un plan"""
        plan_date = Plan_date.objects.create(
            plan_id=self.plan,
            plan_date=date(2025, 5, 1)
        )
        
        # Recuperamos la fecha del plan de la base de datos
        saved_plan_date = Plan_date.objects.get(plan_date=date(2025, 5, 1))

        # Verificamos los valores
        self.assertEqual(saved_plan_date.plan_id.name, 'Escapada a la playa')
        self.assertEqual(saved_plan_date.plan_date, date(2025, 5, 1))
