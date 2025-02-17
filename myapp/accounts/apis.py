
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
# from myapp.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

@api_view(["POST"])
@permission_classes([AllowAny])
def user_signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data["password"])  # Hash the password
        user.save()

        return Response({
            "success": True,
            "data": UserSerializer(user).data,
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
            "message": "Email and password are required.",
            "code": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        return Response({
            "success": True,
            "message": "Login successful.",
            "data": UserSerializer(user).data,
            "code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    return Response({
        "success": False,
        "message": "Invalid email or password.",
        "code": status.HTTP_401_UNAUTHORIZED
    }, status=status.HTTP_401_UNAUTHORIZED)
