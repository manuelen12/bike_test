# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
# Imports from your apps
from common.utils import default_responses
from .api import Controller
from .serializers import (PlansSerializer, UpdatePlansSerializer,
                          UpdatePlansUserSerializer,
                          UpdatePlansUserStatusSerializer,
                          StatusPlansUserSerializer)


class ControlPlan(viewsets.ViewSet):

    serializer_class = PlansSerializer
    """
    SECTION OF PLANS
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.create_plan()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_plans()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = UpdatePlansSerializer

        return default_responses(200, pk)

    def update(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.update_plan(pk)
        if serializer.error:
            print(serializer.error)
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)

    def destroy(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.delete_plan(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class ControlPlansUser(viewsets.ViewSet):

    serializer_class = UpdatePlansUserSerializer
    """
    SECTION OF PLANS
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.update_plan_change()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_plans_user()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = UpdatePlansUserStatusSerializer
        serializer = Controller(request)
        serializer.get_plans_user(pk)
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def update(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.plans_user(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)

    def destroy(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.delete_payment(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class StatusPlansUser(viewsets.ViewSet):

    """
    SECTION OF PLANS
    """
    serializer_class = StatusPlansUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.payment_plans_user()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_plans_user()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        self.serializer_class = UpdatePlansUserStatusSerializer

        return default_responses(200, pk)

    # def update(self, request, pk, *args, **kwargs):
    #     print("1")
    #     serializer = Controller(request)

    #     serializer.payment_plans_user(pk)
    #     if serializer.error:
    #         print(serializer.error)
    #         return default_responses(404, serializer.error)

    def destroy(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.delete_payment(pk)
        if serializer.error:
            return default_responses(404, serializer.error)

        return default_responses(200, serializer.result)


class UserStadistics(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_user_staditics()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)


class PaymentsStadistics(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.payments_stadistics()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)
