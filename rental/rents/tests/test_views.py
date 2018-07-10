# from django.urls import reverse
# from rest_framework import status
from rest_framework.test import APITestCase
# from myproject.apps.core.models import Account
# from os import remove
# pytestmask = pytest.mark.django_db


class FilesTests(APITestCase):
    fixtures = ['rental/rents/fixtures/price_by_frecuency.json']

    def test_bike_is_required(self):
        data = {"bikes": '[{"price_by_frecuency_id": 1, "quantity": 1}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'raise': [{'field': 'Bike', 'error': 'is required'}]})

    def test_price_by_frecuency_id_required(self):
        data = {"bike": '[{"price_by_frecuency_i": 1, "quantity": 1}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'raise': [{'field': 'Price_By_Frecuency_Id', 'error': 'is required'}]})

    def test_quantity_required(self):
        data = {"bike": '[{"price_by_frecuency_id": 1, "quantit": 1}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'raise': [{'field': 'Quantity', 'error': 'is required'}]})

    def test_is_not_exists(self):
        data = {"bike": '[{"price_by_frecuency_id": 12, "quantity": 1}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(), {
                "raise": [
                    {
                        "field": "Price_By_Frecuency_Id",
                        "error": "it is not exit"
                    }
                ]
            })



