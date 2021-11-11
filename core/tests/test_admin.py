from django.forms.fields import EmailField
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class AdminTestCases(TestCase):

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email='testadmin@gmail.com',
            password='testadminpassword')

        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpassword',
            name='testname',
            )

        self.client = Client()
        self.client.force_login(self.admin_user)
        

    def test_users_listed(self):
        url = reverse_lazy('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    
    def test_user_change_page(self):
        url = reverse_lazy('admin:core_user_change', args=(self.user.id,))
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    
    def test_user_add_page(self):
        url = reverse_lazy('admin:core_user_add')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)
