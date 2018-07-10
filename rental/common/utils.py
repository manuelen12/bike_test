# Stdlib imports
import hashlib
import random
import re
from datetime import datetime
from json import loads, dumps
import math
import string
from math import radians, cos, sin, asin, sqrt
# Core Django imports
from django.utils.translation import ugettext_lazy as _, activate
# Third-party app imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework import routers
# Imports from your apps


class Base():
    def __init__(self, request=None):
        self.error = {}
        self.request = request
        self.status = 200
        self.zone_horaria = None
        self.date_now = None
        self.id_resource = None
        self.result = {}

    def valid_data(self):
        if self.request.method == "POST":
            __value = loads(dumps(self.request.data))
        if self.request.method == "GET":
            __value = loads(dumps(self.request.data))
        if self.request.method == "PUT":
            __value = loads(dumps(self.request.data))
        if self.request.method == "DELETE":
            __value = loads(dumps(self.request.data))
        return __value

    def _list_int_info(self, kwargs, lists):
        if not self._list_basic_info(kwargs, lists):
            return False
        for i in lists:
            if not kwargs.get(i):
                self._error_info(i, 'is required')
            self._is_number_int(kwargs[i], i)
        if self.error:
            return False
        return True

    def _is_number_int(self, number, key, max_int=13):

        try:
            number = int(number)
        except:
            self._error_info(key, 'this is not a number')
            return
        return True

    def _basic_info(self, key, objects, keyInfo, valueInfo="is required", error=None, info=False, father=None, index=[], **kwargs):
        if self._basic_required(key, objects):
            return True
        else:
            __errorT = error if not error is None else None
            if info:
                self._error_info(keyInfo, valueInfo, error=__errorT, father=father, index=index, **kwargs)
            else:
                self._data_error(__errorT, keyInfo, valueInfo)
            # if error: self._data_error(error, keyInfo, valueInfo)
            # else: self._data_error(self.error, keyInfo, valueInfo)

    def _basic_required(self, key, objects):
        if self._data_in_objects(key, objects):
            if self._data_existente(key, objects):
                return True

    def _data_in_objects(self, key, objects):
        if key in objects:
            return True

    def _data_existente(self, key, objects):
        if isinstance(objects[key], list) or isinstance(objects[key], dict):
            if objects[key]: return True
        else:
            if not objects[key] is None:
                # if isinstance(objects[key], int) or isinstance(objects[key], float):
                    # if objects[key]: return True
                # else:
                try:
                    if len(str(objects[key])): return True
                except:
                    if len(objects[key]): return True


    def _error_info(self, key, value='data not valid', father=None, error=None, index=[], status=404, **kwargs):
        self.status = status
        if  isinstance(value, str):
            value = str(_(value))

        if  isinstance(value, str):
            key = str(_(key)).title()

        if not isinstance(self.error, list): self.error = []
        __errorT = self.error

        __dic = {'field': key, 'error': value}

        __errorT.append(__dic)

    # def _images(self, img, key, info=None, father=None, index=[], **kwargs):
        data = []
        error = False
        # if not isinstance(img, list):
        #     img = [img]
        # if img:
        #     for i in img:
        #         try: i = int(i)
        #         except:
        #             x_t = urllib2.urlopen(i)
        #             __ext = dict(x_t.info())['content-type']
        #             if not __ext in ['image/jpeg', 'image/png']:
        #                 error = True
        #                 break
        #         data.append(i)
        if error:
            # self._data_error(self.error, key, unicode(_("format not valid")))
            # __errorT = error if not error is None else self.error
            if info:
                self._error_info(key, 'format not valid', father=father, index=index, **kwargs)
            else:
                self._data_error(key=key, value='format not valid')
        else:
            return data

    def _list_basic_info(self, data, lists, name_dict=None):
        if not isinstance(data, dict):
            self._data_error(key=name_dict, value='Must be a dict')
            return False

        __valid = True
        for i in lists:
            if not self._basic_info(i, data, i, info=True, father=name_dict):
                __valid = False
        return __valid

    def export_attr(self, Model, kwargs):
        # import ipdb; ipdb.set_trace()
        __model_attr = [i.name+"_id" if i.many_to_one else i.name for i in Model._meta.get_fields()]
        __values = {}

        for k, v in kwargs.items():
            if k in __model_attr:
                __values.update({str(k): v})
        self.values = __values


CODES = {
    "100": status.HTTP_100_CONTINUE,
    "101": status.HTTP_101_SWITCHING_PROTOCOLS,
    "200": status.HTTP_200_OK,
    "201": status.HTTP_201_CREATED,
    "202": status.HTTP_202_ACCEPTED,
    "203": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    "204": status.HTTP_204_NO_CONTENT,
    "205": status.HTTP_205_RESET_CONTENT,
    "206": status.HTTP_206_PARTIAL_CONTENT,
    "207": status.HTTP_207_MULTI_STATUS,
    "300": status.HTTP_300_MULTIPLE_CHOICES,
    "301": status.HTTP_301_MOVED_PERMANENTLY,
    "302": status.HTTP_302_FOUND,
    "303": status.HTTP_303_SEE_OTHER,
    "304": status.HTTP_304_NOT_MODIFIED,
    "305": status.HTTP_305_USE_PROXY,
    "306": status.HTTP_306_RESERVED,
    "307": status.HTTP_307_TEMPORARY_REDIRECT,
    "400": status.HTTP_400_BAD_REQUEST,
    "401": status.HTTP_401_UNAUTHORIZED,
    "402": status.HTTP_402_PAYMENT_REQUIRED,
    "403": status.HTTP_403_FORBIDDEN,
    "404": status.HTTP_404_NOT_FOUND,
    "405": status.HTTP_405_METHOD_NOT_ALLOWED,
    "406": status.HTTP_406_NOT_ACCEPTABLE,
    "407": status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    "408": status.HTTP_408_REQUEST_TIMEOUT,
    "409": status.HTTP_409_CONFLICT,
    "410": status.HTTP_410_GONE,
    "411": status.HTTP_411_LENGTH_REQUIRED,
    "412": status.HTTP_412_PRECONDITION_FAILED,
    "413": status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    "414": status.HTTP_414_REQUEST_URI_TOO_LONG,
    "415": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    "416": status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    "417": status.HTTP_417_EXPECTATION_FAILED,
    "422": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "423": status.HTTP_423_LOCKED,
    "424": status.HTTP_424_FAILED_DEPENDENCY,
    "428": status.HTTP_428_PRECONDITION_REQUIRED,
    "429": status.HTTP_429_TOO_MANY_REQUESTS,
    "431": status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    "451": status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    "500": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "501": status.HTTP_501_NOT_IMPLEMENTED,
    "502": status.HTTP_502_BAD_GATEWAY,
    "503": status.HTTP_503_SERVICE_UNAVAILABLE,
    "504": status.HTTP_504_GATEWAY_TIMEOUT,
    "505": status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    "507": status.HTTP_507_INSUFFICIENT_STORAGE,
    "511": status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
}


def default_responses(code=int, data=None):

    if data or isinstance(data, list) or isinstance(data, dict):
        if code == 200:
            return Response(data, status=CODES[str(code)])
        else:
            return Response({"raise": data}, status=CODES[str(code)])
    else:
        return Response(status=CODES[str(code)])


class DefaultRouter(routers.DefaultRouter):
    """
    Extends `DefaultRouter` class to add a method for extending url routes from another router.
    """
    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)
