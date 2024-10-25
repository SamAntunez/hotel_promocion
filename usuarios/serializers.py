from django.contrib.auth.models import User
from rest_framework import serializers

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        # Verificar si el nombre de usuario ya está registrado
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está registrado.")
        return value

    def validate_email(self, value):
        # Verificar si el email ya está registrado
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo y/o usuario ya está registrado.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Encripta la contraseña
        user.save()
        return user
