import re

from rest_framework import serializers

from api_gateway.models import User, InternalException


class UserSerializer(serializers.Serializer):
    """
        Serializer for model User.
    """
    username = serializers.CharField(required=True)
    mailbox_address = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        # Validation patterns for username and password
        username_pattern = r'^[a-zA-Z0-9 _\-]+$'
        password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>?/]).{8,}$'

        # Validation process of username and password fields
        if not re.match(username_pattern, attrs.get('username')):
            raise InternalException({"status": 0, "error": "Username contains invalid characters."}, 422)
        if not re.match(password_pattern, attrs.get("password")):
            raise InternalException({"status": 0, "error": "Password must contain 8 characters and at least one number,"
                                                           " one letter and one special character."}, 422)

        # Check if users with this username or mailbox already exist
        if self.Meta.model.objects.filter(username=attrs.get('username')).exists():
            raise InternalException({"status": 0, "error": "Username already exists."}, 409)
        if self.Meta.model.objects.filter(mailbox_address=attrs.get('mailbox_address')).exists():
            raise InternalException({"status": 0, "error": "Email address already exists."}, 409)

        return attrs

    def create(self, validated_data: dict):
        # Create user object without password
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)

        # Add hash password to model
        instance.password = instance.create_password_hash(password)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.mailbox_address = validated_data.get('mailbox_address', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        return instance
