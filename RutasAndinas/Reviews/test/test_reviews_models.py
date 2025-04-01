from django.test import TestCase
from Reviews.models import Review
from Plans.models import Plan,Category
from Users.models import User

class ReviewModelTest(TestCase):
    def setUp(self):
        """Configura un usuario, una categoría y un plan para usar en los tests"""
        # Crear una categoría
        self.category = Category.objects.create(category="Aventura")

        # Crear un usuario
        self.user = User.objects.create_user(
            username="yamin", 
            email="yamin@gmail.com", 
            password="1234", 
            name="Yamin", 
            last_name="Sanchez"
        )

        # Crear un plan y asignarle la categoría
        self.plan = Plan.objects.create(
            category_id=self.category,  # Usar la instancia de Category
            name="Escapada a la playa",
            description="Un plan de aventura en la playa.",
            price=150000,
            places=20,
            has_transport=True,
            has_meal=False,
            has_guide=True
        )

    def test_create_review(self):
        """Prueba la creación de una reseña para un plan"""
        review = Review.objects.create(
            content="Excelente plan para relajarse en la playa.",
            rate=5,
            plan_id=self.plan,
            user_id=self.user
        )

        # Recuperamos la reseña de la base de datos
        saved_review = Review.objects.get(review_id=review.review_id)

        # Verificamos los valores
        self.assertEqual(saved_review.content, 'Excelente plan para relajarse en la playa.')
        self.assertEqual(saved_review.rate, 5)
        self.assertEqual(saved_review.plan_id.name, 'Escapada a la playa')
        self.assertEqual(saved_review.user_id.username, 'yamin')
        self.assertEqual(saved_review.user_id.name, 'Yamin')
