
from . import views

from django.urls import path
app_name = 'auth'

urlpatterns = [
    path('users/create/', views.RegisterUserApiView.as_view(), name='users.create'),
]