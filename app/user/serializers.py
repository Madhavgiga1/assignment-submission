from rest_framework import serializers

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields=['phone','password']
        


    def create(self,validated_data):
       
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self,instance,validated_data):
       
        password = validated_data.pop('password')
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


###serializers.Serializer, which is a basic serializer class in Django REST Framework. Unlike ModelSerializer, this doesn't automatically create fields based on a model.
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=phone,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
  
