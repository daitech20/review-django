from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Review, Store


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include

        data.update({'id': self.user.id})
        data.update({'user': self.user.username})
        data.update({'email': self.user.email})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'is_superuser': self.user.is_superuser})

        users_in_group = Group.objects.get(name="Store").user_set.all()
        if self.user in users_in_group:
            data.update({'group': 'store'})
        # and everything else you want to send in the response
        return data

class CustomJWTSerializer(MyTokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        # This is answering the original question, but do whatever you need here.
        # For example in my case I had to check a different model that stores more user info
        # But in the end, you should obtain the username to continue.
        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)