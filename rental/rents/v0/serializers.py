# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
# Third-party app imports
from rest_framework import serializers
# Imports from your apps

User = get_user_model()


class RentSerializer(serializers.Serializer):

    user_id = serializers.SlugRelatedField(
                queryset=User.objects.all(), slug_field='id')
    bike = serializers.CharField(
        help_text='[{"price_by_frecuency_id": 1, "quantity": 1}]')
