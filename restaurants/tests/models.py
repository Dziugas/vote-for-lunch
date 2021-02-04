from django.test import TestCase
from restaurants.models import Restaurant, Vote


class TestModels(TestCase):
    def test_model_str(self):
        pizzeria = Restaurant.objects.create(name="Toms Pizza")
        vote = Vote.objects.create(ip_address="111.11.111.11",
                                   restaurant=pizzeria, weight=1)
        self.assertEqual(str(pizzeria), "Toms Pizza")
        self.assertEqual(str(vote), "Toms Pizza")
