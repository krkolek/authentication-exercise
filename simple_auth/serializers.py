from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from .models import LoginDetails


class RegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key', read_only=True)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        ModelClass = self.Meta.model
        user = ModelClass.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    class Meta:
        model = get_user_model()
        fields = ('token', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True}
        }


class LoginSerializer(AuthTokenSerializer):
    def create(self, validated_data):
        login_detail = LoginDetails(user=validated_data['user'], ip=self.context['request'].META['REMOTE_ADDR'])
        login_detail.save()
        Token.objects.get_or_create(user=validated_data['user'])
        return validated_data['user']

    def to_representation(self, instance):
        response_list = instance.login_details.all().order_by('login_datetime').values_list('login_datetime', flat=True)
        return {
            'token': instance.auth_token.key,
            'previous_entries': response_list
        }
