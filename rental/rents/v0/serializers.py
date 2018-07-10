# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
# Third-party app imports
from rest_framework import serializers
# Imports from your apps

User = get_user_model()


class RentSerializer(serializers.Serializer):

    bike = serializers.CharField(
        help_text='[{"price_by_frecuency_id": 1, "quantity": 1}]')
