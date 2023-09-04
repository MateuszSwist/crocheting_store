from .views import CreateUserView 
from django.urls import path

urlpatterns =[
    path('create_user/', CreateUserView.as_view(), name='create_user'),
]