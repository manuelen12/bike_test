from rest_framework import serializers
# from django.contrib.auth import get_user_model
from koomper.plans.models import (Plans, UserPlan)
# from json import dumps
# User = get_user_model()


class PlansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plans
        fields = ('name', 'description', 'max_users', 'impressions', 'price')


class UpdatePlansSerializer(serializers.Serializer):

    name = serializers.CharField()
    description = serializers.CharField()
    max_users = serializers.IntegerField()
    impressions = serializers.IntegerField()
    price = serializers.IntegerField()


class UpdatePlansUserSerializer(serializers.Serializer):

    plans_id = serializers.SlugRelatedField(
                queryset=Plans.objects.filter(status=True), slug_field='id')


class StatusPlansUserSerializer(serializers.Serializer):

    user_plans_id = serializers.SlugRelatedField(
                queryset=UserPlan.objects.filter(status_payment=False),
                slug_field='id')


class UpdatePlansUserStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(choices=[('process'),
                                              ('not')])

# class CreatePlansUserSerializer(serializers.Serializer):

#     plans_id = serializers.SlugRelatedField(
#                 queryset=Plans.objects.filter(status=True), slug_field='id')
