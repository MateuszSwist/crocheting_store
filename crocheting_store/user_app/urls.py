from .views import(
    CreateUserView, 
    ListUsersView,
    UserInformationView,
    confirm_email_view,
    LogoutView,
    ChangePasswordView,
    LoginView,
    DeleteAccountView
)

from django.urls import path


urlpatterns =[
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('users_list/', ListUsersView.as_view(), name='users_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete_user/', DeleteAccountView.as_view(), name='delete'),

    path('user_information/me',
        UserInformationView.as_view(), name='user_information_me'),

    path('confirm_email', confirm_email_view, name='confirm_email'),
]