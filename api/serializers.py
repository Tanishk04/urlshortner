# serializers.py
from rest_framework import serializers
from .models import User, URL


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['alias', 'long', 'created_at', 'expires_at', 'last_visited', 'user']
        
class URLPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['alias','long']
     
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
    def save(self,**kwargs):
        user = super().save(**kwargs)
        user.is_staff = False
        user.is_superuser = False
        return user
        
            
