from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import (
    CreateUserView,
    ListUsersView,
    UserInformationView,
    confirm_email_view,
    LogoutView,
    ChangePasswordView,
    LoginView,
    DeleteAccountView,
)



urlpatterns = [
    path("create_user/", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login"),
    path("users_list/", ListUsersView.as_view(), name="users_list"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("delete_user/", DeleteAccountView.as_view(), name="delete"),
    path(
        "user_information/me", UserInformationView.as_view(), name="user_information_me"
    ),
    path("confirm_email", confirm_email_view, name="confirm_email"),


    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html', html_email_template_name = 'password_reset_email.html'),name='password-reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),

    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]
