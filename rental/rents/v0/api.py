from common.utils import Base
from koomper.plans.models import (Plans, UserPlan)
from koomper.rotator.models import (Rotator)
# from koomper.plans.models import (UserPlan)
from json import loads
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
# from requests import get
from django.db.models import Q
import paypalrestsdk
from paypalrestsdk import Payment
from django.db.models import Avg, Sum, Count
from django.core.cache import cache
# import logging
User = get_user_model()


class Controller (Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.error = {}
        self.result = []
        self.url_api = settings.HTTP+self.request.META['HTTP_HOST']+"/api/v0/"
        self.data = self.valid_data()

    def valid_create_plan(self, kwargs):
        __valid = [
            'name', 'description', 'max_users', 'impressions',
            'price'
        ]
        if not self._list_basic_info(kwargs, __valid):
            return

        if not self.list_only_string(self.data, ["name"]):
            return

        if not self._list_int_info(self.data, ["max_users", "impressions",
                                               "price"]):
            return

        return True

    def create_plan(self):

        self.data = self.request.data
        print(self.data)
        if not self.valid_create_plan(self.data):
            return

        self.export_attr(Plans, self.data)
        create = Plans.objects.create(**self.values)
        self.get_plans(create.id)

    def get_plans_user(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        if self.request.user.level == 2:
            __filters.update({'user_id': self.request.user.id})
        __search = self.request.GET.get('search')
        self.get_plans_users(__filters, __paginator, __ordening, __search)

    def get_plans_users(self, filters={}, paginator={}, ordening=(), search=None):
        # import ipdb; ipdb.set_trace()
        __array = []
        if search:
            user = UserPlan.objects.filter(**filters).filter(
                    Q(id__icontains=search) |
                    Q(create_at__icontains=search) |
                    Q(month__icontains=search) |
                    Q(plans__id__icontains=search) |
                    Q(plans__name__icontains=search) |
                    Q(plans__price__icontains=search) |
                    Q(plans__description__icontains=search) |
                    Q(plans__max_users__icontains=search) |
                    Q(plans__impressions__icontains=search) |
                    Q(user__name__icontains=search)).order_by(*ordening)
        else:
            user = UserPlan.objects.filter(**filters)
        for i in user:
            __dict = {
                'id': i.id,
                'url': self.url_api+"plans_user/"+str(i.id),
                'status_payment': i.status_payment,
                'create_at': i.create_at,
                "month_id": i.month,
                "month": i.get_month_display(),
                'plans': {
                    'plans_id': i.plans_id,
                    'plans_name': i.plans.name,
                    'plans_price': i.plans.price,
                    'status': i.plans.status,
                    'description': i.plans.description,
                    'max_users': i.plans.max_users,
                    'impressions': i.plans.impressions,
                },
                'user': {
                    'id': i.user_id,
                    'name': i.user.name,
                    'username': i.user.username,
                }
            }

            __array.append(__dict)

        if not filters.get('pk'):
            self.paginator(__array, paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array[0]
        return __array

    def get_plans(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))

        if pk:
            __filters.update({'pk': pk})
        __filters.update({'status': True})
        __array = []
        for i in Plans.objects.filter(**__filters).order_by("price"):
            __dict = {
                'id': i.id,
                'name': i.name,
                'url': self.url_api+"plans/"+str(i.id),
                'status': i.status,
                'description': i.description,
                'max_users': i.max_users,
                'impressions': i.impressions,
                'price': i.price,
                'create_at': i.create_at
            }

            __array.append(__dict)

        if not __filters.get('pk'):
            self.paginator(__array, __paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array[0]
        return __array

    def update_plan(self, id_plan):
        self.data = self.request.data
        print(self.data)
        if not self.valid_create_plan(self.data):
            return
        update = Plans.objects.filter(id=id_plan, status=True)
        if not update:
            self._error_info("ID Plan", "not exit")
            return
        update[0].name = self.data.get('name')
        update[0].description = self.data.get('description')
        update[0].max_users = self.data.get('max_users')
        update[0].impressions = self.data.get('impressions')
        update[0].price = self.data.get('price')
        update[0].save()
        x = self.get_plans(id_plan)
        self.result = x

    def update_plan_change(self):
        # print(self.request.user.id)
        self.data = self.request.data
        __valid = [
            'plans_id'
        ]
        if not self._list_basic_info(self.data, __valid):
            return
        if not self._list_int_info(self.data, ["plans_id"]):
            return
        plans = Plans.objects.filter(id=self.data.get("plans_id"), status=True)
        if not plans:
            self._error_info("Id Plan", "not exit")
            return
        user_plan = UserPlan.objects.get_or_create(
            user_id=self.request.user.id,
            status_payment=False, month=datetime.now().month)
        if not user_plan:
            self._error_info(_("Plan"), _("dont have a plan"))
            return
        user_plan[0].plans_id = self.data.get("plans_id")
        user_plan[0].save()
        x = self.get_plans_user(user_plan[0].id)
        self.result = x

    def delete_payment(self, pk):
        self.data = self.request.data
        user_plan = UserPlan.objects.filter(id=pk,
                                            # user_id=self.request.user.id,
                                            status_payment=False)
        if not user_plan:
            self._error_info(_("Id"), _("do not has plans"))
            return
        UserPlan.objects.filter(id=pk,
                                # user_id=self.request.user.id,
                                status_payment=False).delete()
        self.result = "Delete payment"

    def payment_plans_user(self):
        self.data = self.request.data
        __valid = [
            'user_plans_id'
        ]
        if not self._list_basic_info(self.data, __valid):
            return
        users_plan = UserPlan.objects.filter(id=self.data.get("user_plans_id"),
                                             user_id=self.request.user.id,
                                             status_payment=False)
        if not users_plan:
            self._error_info(_("I"), _("do not has plans"))
            return
        print("hola")
        paypalrestsdk.configure({
            "mode": "live", # sandbox or live
            #"client_id": "AZOdRzhn4mXchn3FgsanK1QulZkS6WN6fFw8T8RlyO-rarF9bdr7BOkc-OQ3z2Juq9jmgD2HYEYJhhig",
            "client_id": "AZUHbzpomWuCMc1soG8zK3ezqt0RMVBHA40dp9VVxZ4a_MFdr4DhFchmcoZ6ogJN7d5TjsvXRQl34H-6",
            #"client_secret": "EPKFQxUyLzTDqG0HCgN8cF3bUnzBuTXltOLA-7NQGRirRQ_CI69ZiZMvJdQRq7yj5wmx1VGrhOuNxJJF"
            "client_secret": "ELPbfxmIQry1szsnFDf7_2Ex1g78KUpjH7bnHuMtvTY6XasHWRh719ft0PDX1IgWGj_26voNCHQM3-d0"
        })
        payment = Payment({
          "intent": "sale",
          "payer": {
            "payment_method": "paypal"
          },
          # Set redirect urls
          "redirect_urls": {
            "return_url": "https://admin.koomper.com/api/v0/validate/",
            "cancel_url": "https://admin.koomper.com/api/v0/validate/"
          },
          # Set transaction object
          "transactions": [{
            "amount": {
              "total": str(users_plan[0].plans.price),
              "currency": "USD"
            },
            "description": "Koomper"
          }]
        })
        # import ipdb; ipdb.set_trace()
        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    print(payment)
                    self.result = redirect_url
        else:
            print("Error while creating payment:")
            print(payment.error)
        print(payment.id)
        cache.set(
            payment.id,
            users_plan[0].id,
            60*60*60
        )

    def plans_user(self, pk):
        self.data = self.request.data
        __valid = [
            'status'
        ]
        if not self._list_basic_info(self.data, __valid):
            return
        up = UserPlan.objects.filter(id=pk,
                                     user_id=self.request.user.id,
                                     status_payment=True)
        if up:
            self._error_info(_("Plans"), _("paid out"))
            return
        if self.data.get("status") == "process":
            users_plan = UserPlan.objects.filter(id=pk,
                                                 user_id=self.request.user.id,
                                                 status_payment=False)
            if not users_plan:
                self._error_info(_("I"), _("do not has plans"))
                return
            users_plan[0].status_payment = True
            users_plan[0].save()
            self.request.user.plans_id = users_plan[0].plans_id
            self.request.user.save()
            x = self.get_plans_user(pk)
            self.result = x
        else:
            print("pay not process")

    def delete_plan(self, plan_id):
        self.data = self.request.data
        if not Plans.objects.filter(id=plan_id):
            self._error_info(_("ID Plan"), _("not exit"))
            return
        delete = Plans.objects.get(id=plan_id)
        delete.status = False
        delete.save()
        x = self.get_plans(delete.id)
        self.result = x

    def get_user_staditics(self):
        # import ipdb; ipdb.set_trace()
        __user = User.objects.filter().count()
        __user_a = Rotator.objects.filter(banner__status=True).values("banner__user_id").annotate(Count('banner__user_id'))
        # print(__user_a)
        User.objects.filter(level=2, status=True).count()
        __user_p = UserPlan.objects.filter(month=datetime.now().month, status_payment=True).count()
        self.result = {
            "total_u": __user,
            "total_active_u": __user_a.count(),
            "user_pay": __user_p,

        }

    def payments_stadistics(self):
        __user = UserPlan.objects.filter(
            status_payment=True).aggregate(
            Sum('plans__price'))["plans__price__sum"]
        __user_a = UserPlan.objects.filter(
            status_payment=True).aggregate(Avg('plans__price'))
        __user_p = UserPlan.objects.select_related(
            "plans").filter(
            create_at__year=datetime.now().year, status_payment=True)
        __count = 0
        __mont = []
        __price = 0
        for i in __user_p:
            __price += i.plans.price
            if i.month not in __mont:
                __mont.append(i.month)
                __count += 1
        __total = (__price / __count) if __price else 0

        self.result = {
            "total_u": __user if __user else 0,
            "average_income": __user_a.get("plans__price__avg", 0) if __user_a.get("plans__price__avg", 0) else 0,
            "user_pay": __total,
            "year": datetime.now().year
        }
