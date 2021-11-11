from logging import PlaceHolder
from django.test import TestCase
from django.urls import reverse_lazy
import rest_framework
from rest_framework.fields import to_choices_dict
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


CREATE_USER_API = reverse_lazy('user:create')
TOKEN_URL = reverse_lazy('user:token')
ME_URL = reverse_lazy('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    

    def test_user_created_successfully(self):
        """This test that the user is created successfully wiht its payload"""
        payload = {
            'email':'testuser@gmail.com',
            'password':'testpassword',
            'name':'testuser'
        }
        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    

    def test_user_exists(self):
        """Test fails if user exists"""
        payload = {
            'email':'testuser@gmail.com',
            'password':'testpassword',
            'name':'testuser'
        }
        user = create_user(**payload)
        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_passowrd_too_short(self):
        """Test fails if the passward is less than 5 length"""
        payload = {
            'email':'testuser@gmail.com',
            'password':'ps',
            'name':'testuser'
        }
        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test given the user and passwoed it return the auth token"""
        payload = {
            'email':'testuser@gmail.com',
            'password':'testpassword',
            'name':'testname'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)    
    
    def test_create_token_invalid_cred(self):
        """Test no token is created for an invalid email or password"""
        payload = {
            'email':'testuser@gmail.com',
            'password':'ps',
        }
        create_user(email='testuser@gmail.com', password='testpassword')
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """Test no token is created if no user exists"""
        payload = {
            'email':'testuser@gmail.com',
            'password':'testpassword',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_no_user(self):
        """Test no token is created if no user exists"""
        payload = {
            'email':'testuser@gmail.com',
            'password':'',
        }
        create_user(email='testuser@gmail.com', password='testpassword')
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_me_for_unauthenticated_user(self):
        """Test the unauthenticated user is not allowed for me url"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test for private users"""

    def setUp(self):
        self.client = APIClient()
        payload = {
            'email':'testuser@gmail.com',
            'password':'testpassword',
            'name':'testname'
        }
        self.user = get_user_model().objects.create_user(**payload)

        self.client.force_authenticate(self.user)
    

    def test_retrieve_user_profile(self):
        """Test the api works for authorize users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_post_me_is_not_allowed(self):
        """Test post call on me url is not allowed"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_updated_user_profile(self):
        """Test authorize user can update their profile"""
        res = self.client.patch(ME_URL, data={'name':'newName', 'password':'newPassword'})
        # print("RES ", res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        # print("USER ", self.user.name)

        self.assertEqual(self.user.name, 'newName')
        self.assertTrue(self.user.check_password('newPassword'))
