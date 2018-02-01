
from django.conf.urls import url, include
from rest_framework import routers
from plans.v0.views import (ControlPlan, ControlPlansUser, StatusPlansUser, UserStadistics, PaymentsStadistics)
from plans.views import (StatusPay)

router = routers.DefaultRouter()

router.register(r'plans', ControlPlan, base_name='plans')
router.register(r'plans_user', ControlPlansUser, base_name='plans_user')
router.register(r'payment_plans', StatusPlansUser, base_name='payment_plans')
router.register(r'user_stadistics', UserStadistics , base_name='user_stadistics')
router.register(r'payments_stadistics', PaymentsStadistics, base_name='payments_stadistics')
router.register(r'validate', StatusPay, base_name='validate')
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^validate/', include('')),
]
