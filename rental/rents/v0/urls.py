# Stdlib imports
# Core Django imports
from django.conf.urls import url, include
# Third-party app imports
from rest_framework import routers
# Imports from your apps
from rental.rents.v0.views import (RentViewSets)

router = routers.DefaultRouter()

router.register(r'rents', RentViewSets, base_name='rents')
# urlpatterns = [
#     url(r'^', include(router.urls)),
# ]
