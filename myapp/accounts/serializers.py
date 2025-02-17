from rest_framework import serializers
from myapp.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ["id", "key", "value", "icon", "sort"]
