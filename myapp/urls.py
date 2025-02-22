from django.urls import path
from .views import Home
from .accounts.apis import user_signup, user_login


urlpatterns = [
    path('', Home.as_view()),
    path('register/', user_signup, name='register'),
    path('login-api/', user_login, name='login'),
]



