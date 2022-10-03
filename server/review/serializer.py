from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Review, Store, Customer, MessageLog
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from allauth.socialaccount.models import SocialApp


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Store
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user':
                         {
                             'id': self.user.id,
                             'username': self.user.username,
                             'email': self.user.email,
                             'first_name': self.user.first_name,
                             'last_name': self.user.last_name,
                             'is_superuser': self.user.is_superuser
                         }
                     })
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

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'is_superuser',]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=attrs['password'])
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


    def create(self, validated_data):
        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError({"username": "User name already exists"})
        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
		
        user.is_superuser = validated_data['is_superuser']
        user.save()

        return user

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class DetailStoreSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=True)
    class Meta:
        model = Store
        fields = '__all__'

class UpdateStoreSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Store
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'username', 'first_name', 'last_name', 'email']
        lookup_field = 'username'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AddCustomerStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')
    
    # def create(self, validated_data):
    #     customers = validated_data.pop('customer')

    #     print(customers)
    #     store = Store.objects.get(store_slug=validated_data.pop('store_slug'))
    #     return store
    def create(self, validated_data):
       
        return super().create(validated_data)

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'new_password1', 'new_password2']

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match"})
        errors = dict()

        try:
            # validate the password and catch the exception
            validators.validate_password(password=attrs['new_password1'])
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['new_password'] = list(e.messages)

        try:
            user = User.objects.get(username=attrs['username'])
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({"password": "Password wrong!"})
        except exceptions.ValidationError as e:
            errors['error'] = "User not found!"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):
        username = validated_data.pop('username')
        user = User.objects.get(username=username)
        user.set_password(validated_data['new_password1'])
        user.save()

        return user

		
class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        errors = dict()

        try:
            # validate the password and catch the exception
            validators.validate_password(password=attrs['password'])
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        try:
            user = User.objects.get(username=attrs['username'])
        except exceptions.ValidationError as e:
            errors['error'] = "User not found!"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):
        username = validated_data.pop('username')
        user = User.objects.get(username=username)
        user.set_password(validated_data['password'])
        user.save()

        return user


class SocialApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialApp
        fields = ['name', 'client_id', 'secret']

class MessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageLog
        fields = ['content',]