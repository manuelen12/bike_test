# Stdlib imports
from json import loads
# Core Django imports
from django.contrib.auth import get_user_model
# Third-party app imports
# Imports from your apps
from rental.common.utils import Base
from rental.rents.models import Rentals, Bike, PriceByFrecuency

User = get_user_model()


class Controller (Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.error = {}
        self.result = []
        self.data = self.valid_data()

    def valid_rent(self, kwargs):
        __valid = [
            'bike'
        ]
        if not self._list_basic_info(kwargs, __valid):
            return

        try:
            kwargs['bike'] = loads(kwargs['bike'])
        except:
            self._error_info("bike", "must be a json")
            return

        __valid = ["price_by_frecuency_id", "quantity"]
        __price_by = []
        __group_bike = {}
        for i in kwargs['bike']:
            if not self._list_int_info(i, __valid):
                return
            if int(i["price_by_frecuency_id"]) in __group_bike:
                __group_bike[i["price_by_frecuency_id"]] += int(i["quantity"])
            else:
                __group_bike[int(i["price_by_frecuency_id"])] = int(i["quantity"])
            __price_by.append(int(i["price_by_frecuency_id"]))
        __price = {i.id: i.price for i in PriceByFrecuency.objects.filter(
            id__in=__price_by)}

        if not __price:
            self._error_info("price_by_frecuency_id", "it is not exit")
            return

        x = sorted(__group_bike.items(), key=lambda kv: __price[kv[0]])
        import ipdb; ipdb.set_trace()
        __total = 0
        __quantity = 0
        bike = []
        for i in kwargs['bike']:
            bike.append(i)
            if 3 <= int(i["quantity"]) <= 5:
                __quantity += int(i["quantity"])
                __total += x[i["price_by_frecuency_id"]]
        kwargs["neto_price"] = __total
        kwargs["total_price"] = __total
        kwargs["familiar_rental_promotion"] = False
        # import ipdb; ipdb.set_trace()
        if 3 <= __quantity <= 5:
            kwargs["total_price"] -= 30 * __total / 100
            kwargs["familiar_rental_promotion"] = True
        return True

    def create_rent(self):
        if not self.valid_rent(self.data):
            return
        # import ipdb; ipdb.set_trace()
        self.export_attr(Rentals, self.data)
        __r = Rentals.objects.create(**self.values)
        # x = __r
        for i in self.data['bike']:
            i["rentals_id"] = __r.id
            self.export_attr(Bike, i)
            Bike.objects.create(**self.values)
        self.list_rent(__r.id)

    def list_rent(self, pk=None):

        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        __search = self.request.GET.get('search')

        self.list_rents(__filters, __paginator, __ordening, __search)

    def list_rents(self, filters={}, paginator={}, ordening=(), search=None):
        __array = []
        __rents = Rentals.objects.prefetch_related("rentals_bike").filter(
            **filters).order_by(*ordening)
        for i in __rents:
            __dict = {
                "neto_price": i.neto_price,
                "total_price": i.total_price,
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
