# Stdlib imports
from json import loads
# Core Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
# Third-party app imports
# Imports from your apps
from common.utils import Base
from rental.rents.models import Rentals

User = get_user_model()


class Controller (Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.error = {}
        self.result = []
        self.url_api = settings.HTTP+self.request.META['HTTP_HOST']+"/api/v0/"
        self.data = self.valid_data()

    def create_rent(self):
        print("pytho")

    def get_rent(self, pk=None):
        print("hh")

    def list_rent(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        __filters.update({"user_id": self.request.user.id})
        __search = self.request.GET.get('search')
        __filters.update({"status": True})
        # __filters.update({"user_id": self.request.user.id})
        self.list_rents(__filters, __paginator, __ordening, __search)

    def list_rents(self, filters={}, paginator={}, ordening=(), search=None):
        __array = []
        __rents = Rentals.objects.filter(**filters)
        for i in __rents:
            __dict = {}
            __array.append(__dict)

        if not filters.get('pk'):
            # import ipdb; ipdb.set_trace()
            self.paginator(__array, paginator)
            print(paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array[0]
