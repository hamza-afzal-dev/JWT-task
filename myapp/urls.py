# from django.urls import path
# from .views import Home
# from .accounts.apis import user_signup, user_login


# urlpatterns = [
#     path('', Home.as_view()),
#     path('register/', user_signup, name='register'),
#     path('login-api/', user_login, name='login'),
# ]


from django.urls import path
from .views import (
    Home,
    AddUser,
    UserList,
    UpdateUser,
    DeleteUser,
    GoogleLogin,
    GoogleLoginCallback,
    LoginPage,
)
from .accounts.apis import user_signup, user_login  # Adjusted import path

urlpatterns = [
    # API Endpoints
    path("", Home.as_view(), name="home"),
    path("register/", user_signup, name="register"),
    path("login-api/", user_login, name="login"),

    # Google OAuth
    path("login/", LoginPage.as_view(), name="login_page"),
    path("google-login/", GoogleLogin.as_view(), name="google_login"),
    path("google-callback/", GoogleLoginCallback.as_view(), name="google_callback"),

    # CRUD Operations for Users
    path("users/", UserList.as_view(), name="user_list"),
    path("users/add/", AddUser.as_view(), name="add_user"),
    path("users/update/<int:user_id>/", UpdateUser.as_view(), name="update_user"),
    path("users/delete/<int:user_id>/", DeleteUser.as_view(), name="delete_user"),
]
