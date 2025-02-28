from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from urllib.parse import urljoin
import requests
from django.urls import reverse
from rest_framework import status
from .accounts.forms import UserForm  # Ensure this exists
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

User = get_user_model()

### --------------------------- Django Views for CRUD --------------------------- ###



class AddUser(View):
    """Create a new user via form."""
    def get(self, request):
        form = UserForm()
        return render(request, "add_user.html", {"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.password = make_password(form.cleaned_data["password"])  # Hash password
            user.save()  # Save user with hashed password
            return redirect("user_list")
        return render(request, "add_user.html", {"form": form})

class UserList(View):
    """Display a list of users with search and pagination."""
    def get(self, request):
        query = request.GET.get("q", "").strip()
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).order_by("id")

        # Pagination (Show 5 users per page)
        paginator = Paginator(users, 5)
        page_number = request.GET.get("page")

        try:
            page_obj = paginator.get_page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.get_page(1)  # Default to first page if invalid

        return render(request, "user_list.html", {"users": page_obj})


class UpdateUser(View):
    """Update an existing user's information."""
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserForm(instance=user)
        return render(request, "update_user.html", {"form": form, "user": user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_list")
        return render(request, "update_user.html", {"form": form, "user": user})


class DeleteUser(View):
    """Delete a user."""
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, "delete_user.html", {"user": user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect("user_list")


### --------------------------- API Views (JWT & Google Login) --------------------------- ###

class Home(APIView):
    """JWT-Protected Home API."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, World!"})


class GoogleLogin(SocialLoginView):
    """Google OAuth2 Login API."""
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    """Google OAuth2 Callback API."""
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Missing authorization code"}, status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = urljoin(settings.BASE_URL, reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        if response.status_code != 200:
            return Response({"error": "Google authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(response.json(), status=status.HTTP_200_OK)


class LoginPage(View):
    """Login Page View."""
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
