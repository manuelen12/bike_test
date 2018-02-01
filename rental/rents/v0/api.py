# Stdlib imports
from json import loads
# Core Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
# Third-party app imports
# Imports from your apps
from common.utils import Base
from rental.rents.models import Rentals, Bike, PriceByFrecuency

User = get_user_model()


class Controller (Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.error = {}
        self.result = []
        self.url_api = settings.HTTP+self.request.META['HTTP_HOST']+"/api/v0/"
        self.data = self.valid_data()

    def valid_rent(self, kwargs):
        __valid = [
            'user_id', 'bike'
        ]
        if not self._list_basic_info(kwargs, __valid):
            return

        try:
            kwargs['bike'] = loads(kwargs['bike'])
        except:
            self._error_info("bike", "must be a json")
            return

        x = {i.id: i.price  for i in PriceByFrecuency.objects.filter(id__in=[e["price_by_frecuency_id"] for e in kwargs["bike"]])}
        print(x)
        if not x:
            self._error_info("price", "it i not exit")
            return

        __total = 0
        for i in kwargs['bike']:
            __valid = ["price_by_frecuency_id", "quantity"]
            if not self._list_basic_info(i, __valid):
                return
            __total += x[i["price_by_frecuency_id"]]
        kwargs["neto_price"] = __total

        if 3<=len(kwargs['bike'])<=5:
            kwargs["total_price"] = 30 * __total/ 100
            kwargs["familiar_rental_promotion"] = True
        else:
            kwargs["total_price"] = __total
            kwargs["familiar_rental_promotion"] = False
        return True

    def create_rent(self):
        if not self.valid_rent(self.data):
            return
        self.export_attr(Rentals, self.data)
        __r = Rentals.objects.create(**self.values)
        for i in self.data['bike']:
            self.export_attr(Bike, i)
            i["rentals_id"] = __r.id
            Bike.objects.create(**i)
        self.list_rent(__r.id)

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
        __rents = Rentals.objects.prefetch_related("rentals_bike").filter(
            **filters).order_by(*ordening)
        for i in __rents:
            __dict = {
                "user": {
                    "username": i.user.username
                },
                "neto_price": i.neto_price,
                "total_price": i.total_price,
                "familiar_rental_promotion": i.familiar_rental_promotion,
                "status": i.status,
                "create_at": str(i.create_at),
                "bike": []
            }
            for e in i.rentals_bike.all():
                __dict2 = {
                    "price_by_frecuency_id": e.price_by_frecuency_id,
                    "quantity": e.quantity,
                    "create_at": e.create_at,
                }
                __dict['bike'].append(__dict2)

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
