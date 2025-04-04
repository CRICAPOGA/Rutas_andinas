from django.test import TestCase
from Users.models import User, Role

class UserModelTest(TestCase):
    def setUp(self):
        """Configura un Role para usar en los tests"""
        self.role = Role.objects.create(role="turista")

    def test_create_user(self):
        """Prueba la creación de un usuario con su rol"""
        user = User.objects.create_user(
            username='yamin',
            email='yamin@gmail.com',
            password='1234'
        )
        user.name = 'Yamin'
        user.last_name = 'Sanchez'
        user.role_id = self.role  # Asignamos el rol al usuario
        user.save()

        # Recuperamos el usuario de la base de datos
        saved_user = User.objects.get(username='yamin')

        # Verificamos los valores
        self.assertEqual(saved_user.name, 'Yamin')
        self.assertEqual(saved_user.last_name, 'Sanchez')
        self.assertEqual(saved_user.username, 'yamin')
        self.assertEqual(saved_user.email, 'yamin@gmail.com')
        self.assertEqual(saved_user.role_id.role, 'turista')
