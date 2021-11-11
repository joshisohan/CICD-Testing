from user import views
from django.urls import path

app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name="create"),
    path('token/', views.AuthTokenView.as_view(), name='token'),
    path('update/', views.UpdateUserView.as_view(), name='me')
]
