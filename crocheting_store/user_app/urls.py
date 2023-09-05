from .views import(
    CreateUserView, 
    ListUsersView,
    UserInformationView,
    confirm_email_view,
)

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns =[
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('login/', obtain_auth_token, name='login'),
    path('users_list/', ListUsersView.as_view(), name='users_list'),
    
    path('user_information/me',
        UserInformationView.as_view(), name='user_information_me'),

    path('confirm_email', confirm_email_view, name='confirm_email'),
]