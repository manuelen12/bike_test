# from django.urls import reverse
# from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from rental.rents.models import Bike, PriceByFrecuency, Rentals
# from myproject.apps.core.models import Account
# from os import remove
# pytestmask = pytest.mark.django_db


class FilesTests(APITestCase):
    fixtures = ['rental/rents/fixtures/price_by_frecuency.json']

    def test_get_empty_bike(self):
        data = {"bike": 'Carcas'}
        response = self.client.get("/api/v0/rents/", data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json(),
            {'result': 'empty'})

    def test_bike_must_be_json(self):
        data = {"bike": 'Carcas'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'raise': [{'field': 'Bike', 'error': 'must be a json'}]})

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

    def test_quantity(self):
        data = {"bike": '[{"price_by_frecuency_id": 1, "quantity": 6}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'raise': [{'error': 'must be less than 5', 'field': 'Quantity'}]})

    def test_without_promotion_1(self):
        data = {"bike": '[{"price_by_frecuency_id": 1, "quantity": 1}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["neto_price"], 20)
        self.assertEqual(response.json()["total_price"], 20)
        self.assertEqual(response.json()["familiar_rental_promotion"], False)

    def test_without_promotion_2(self):
        data = {"bike": '[{"price_by_frecuency_id": 1, "quantity": 2}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["neto_price"], 40)
        self.assertEqual(response.json()["total_price"], 40)
        self.assertEqual(response.json()["familiar_rental_promotion"], False)

    def test_without_promotion_3(self):
        data = {"bike": '[{"price_by_frecuency_id": 1, "quantity": 1}, {"price_by_frecuency_id": 2, "quantity": 1}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["neto_price"], 80)
        self.assertEqual(response.json()["total_price"], 80)
        self.assertEqual(response.json()["familiar_rental_promotion"], False)

    def test_promotion_1(self):
        data = {"bike": '[{"price_by_frecuency_id": 1, "quantity": 5}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["neto_price"], 100)
        self.assertEqual(response.json()["total_price"], 70)
        self.assertEqual(response.json()["familiar_rental_promotion"], True)

    def test_promotion_2(self):
        data = {"bike": '[{"price_by_frecuency_id": 1, "quantity": 1}, {"price_by_frecuency_id": 2, "quantity": 1}, {"price_by_frecuency_id": 3, "quantity": 1}]'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["neto_price"], 85)
        self.assertEqual(response.json()["total_price"], 59.5)
        self.assertEqual(response.json()["familiar_rental_promotion"], True)

    def test_get_bikes(self):
        mixer.blend(Bike)
        response = self.client.get("/api/v0/rents/")
        self.assertEqual(response.status_code, 200)

    def test_get_bike(self):
        bike = mixer.blend(Bike)
        response = self.client.get("/api/v0/rents/"+str(bike.id)+"/")
        self.assertEqual(response.status_code, 200)

    def test_get_bad_bike(self):
        response = self.client.get("/api/v0/rents/50/")
        self.assertEqual(response.status_code, 200)
