
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def user_signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data["password"])  # Hash the password
        user.save()

        tokens = get_tokens_for_user(user)

        return Response({
            "success": True,
            "Message": "User Created successfully",
            "data": UserSerializer(user).data,
            "tokens": tokens,
            "code": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)

    return Response({
        "success": False,
        "errors": serializer.errors,
        "code": status.HTTP_400_BAD_REQUEST
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({
            "success": False,
            "message": "username and password are required.",
            "code": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        tokens = get_tokens_for_user(user)
        return Response({
            "success": True,
            "message": "Login successful.",
            "data": UserSerializer(user).data,
            "tokens": tokens,
            "code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    return Response({
        "success": False,
        "message": "Invalid username or password.",
        "code": status.HTTP_401_UNAUTHORIZED
    }, status=status.HTTP_401_UNAUTHORIZED)
