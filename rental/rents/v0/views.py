# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
# Imports from your apps
from rental.common.utils import default_responses
from .api import Controller
from .serializers import (RentSerializer)


class RentViewSets(viewsets.ViewSet):

    serializer_class = RentSerializer
    """
    SECTION OF PLANS
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.create_rent()

        if serializer.error:
            return default_responses(404, serializer.error)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.list_rent()

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.list_rent(pk)

        return default_responses(200, serializer.result)
