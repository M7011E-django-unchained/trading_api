from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']
        # TODO set min length later
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True}}

        def create(self, validated_data):
            return get_user_model().objects.create_user(**validated_data)
