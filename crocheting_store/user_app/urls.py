from .views import(
    CreateUserView, 
    ListUsersView,
    SendEmailConfirmationTokenView,
    UserInformationView
)
from django.urls import path

urlpatterns =[
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('users_list/', ListUsersView.as_view(), name='users_list'),
    path('user_information/me',
        UserInformationView.as_view(), name='user_information_me'),
    path('send_confirmation_email/',
        SendEmailConfirmationTokenView.as_view(), name='send_email_confirmation_token'),
]