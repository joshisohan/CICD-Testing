from logging import PlaceHolder
from django.forms.fields import EmailField
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag, Ingredient


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """

        email = "sohanjoshi@gmail.com"
        password = "sohanjoshi"

        user = get_user_model().objects.create_user(
                email=email,
                password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_is_normalize(self):
        """Test if the email is normalize or not """

        email = "sohan@GMAIL.COM"
        password = 'test123'

        user = get_user_model().objects.create_user(email, password)
        
        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):

        """Test if new user email is blank or not valid """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='test123')

    def test_create_superuser(self):
        """Test if a user is created as super user """

        email = 'sohan@gmail.com'
        password = "test123"

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_model_is_working(self):
        """Test tag model is creating the tags given the inputs"""
        name = 'Vegan'

        tag = Tag.objects.create(
            user=get_user_model().objects.create_user(
                email='test@email.com',
                password='testpassword',
            ),
            name=name)
        
        self.assertEqual(str(tag), name)
    
    def test_ingredients_model_str(self):
        """Test string repr of ingredients model is same as name"""
        email = "sohanjoshi@gmail.com"
        password = "sohanjoshi"

        user = get_user_model().objects.create_user(
                email=email,
                password=password
            )
        paylod = {'name':'testIngridients'}
        ingridients = Ingredient.objects.create(user=user, name=paylod['name'])

        self.assertEqual(str(ingridients), paylod['name'])



