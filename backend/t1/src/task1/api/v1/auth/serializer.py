from rest_framework import serializers
from web.models import User
import re
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'date_joined', 'last_login')

    def validate_phone(self, value):
        if value and not re.match(r'^\+\d{10,15}$', value):
            raise serializers.ValidationError("Enter a valid international phone number starting with '+'.")
        return value

    def validate_email(self, value):
        try:
            django_validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

