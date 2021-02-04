from datetime import datetime, timedelta, date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurants.models import Restaurant, Vote
from restaurants.views import vote_limit


class RestaurantTests(APITestCase):
    def test_create_restaurant_endpoint(self):
        restaurant_data = {
        "name": "Jerrys Pizza"
        }
        restaurant_create_url = reverse("restaurants:restaurant-list")
        response = self.client.post(restaurant_create_url, data=restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)


    def test_restaurant_history_endpoint(self):
        restaurant = Restaurant.objects.create(name="Peters Pizza")
        vote_url = reverse("restaurants:vote")
        vote_data = self.vote_data = {
            "restaurant": restaurant.id
        }
        history_url = reverse("restaurants:history", args=(restaurant.id,))

        for i in range(0, 5):
            self.client.post(vote_url, data=vote_data)

        dt = datetime.now()
        todays_date = dt.date()
        response = self.client.get(history_url)
        self.assertEqual(response.data[0]["date"], todays_date)
        self.assertEqual(response.data[0]["total_votes"], 2.25)


    def test_history_endpoint_displays_latest_date_first(self):
        restaurant1 = Restaurant.objects.create(name="Toms Pizza")
        history_url = reverse("restaurants:history", args=(restaurant1.id,))

        # create one vote for today
        Vote.objects.create(ip_address="111.11.111.11", restaurant=restaurant1, weight=1)
        # create one vote for yesterday
        vote_2 = Vote.objects.create(ip_address="111.11.111.11", restaurant=restaurant1, weight=1)
        yesterday = datetime.now()-timedelta(days=1)
        Vote.objects.filter(id=vote_2.id).update(date=yesterday)
        # create one vote for last week
        vote_3 = Vote.objects.create(ip_address="111.11.111.11", restaurant=restaurant1, weight=1)
        last_week = datetime.now()-timedelta(days=7)
        Vote.objects.filter(id=vote_3.id).update(date=last_week)

        response = self.client.get(history_url)
        print(response.data)
        self.assertEqual(response.data[0]["date"], date(2021, 2, 4))
        self.assertEqual(response.data[2]["date"], date(2021, 1, 28))


    def test_restaurant_with_most_votes_is_on_top(self):
        restaurant_url = reverse("restaurants:restaurant-list")
        restaurant1 = Restaurant.objects.create(name="Toms Pizza")
        restaurant2 = Restaurant.objects.create(name="Jerrys Pizza")
        restaurant3 = Restaurant.objects.create(name="Peters Pizza")

        Vote.objects.create(ip_address="111.11.111.11", restaurant=restaurant1, weight=1)
        Vote.objects.create(ip_address="111.11.111.11", restaurant=restaurant2, weight=0.25)

        response = self.client.get(restaurant_url)
        self.assertEqual(response.data[0]["name"], "Toms Pizza")


    def test_restaurant_with_null_votes_is_listed_last(self):
        restaurant_url = reverse("restaurants:restaurant-list")
        restaurant1 = Restaurant.objects.create(name="Toms Pizza")
        restaurant2 = Restaurant.objects.create(name="Jerrys Pizza")
        restaurant3 = Restaurant.objects.create(name="Peters Pizza")

        Vote.objects.create(ip_address="111.11.111.11", restaurant=restaurant1, weight=1)
        Vote.objects.create(ip_address="111.11.111.11", restaurant=restaurant2, weight=0.25)

        response = self.client.get(restaurant_url)
        self.assertEqual(response.data[2]["name"], "Peters Pizza")       


class VoteTests(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Toms Pizza")
        self.vote_url = reverse("restaurants:vote")
        self.vote_data = {
            "restaurant": self.restaurant.id
        }


    def test_vote_1_time(self):        
        response = self.client.post(self.vote_url, data=self.vote_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Voted successfully")
        
        vote = Vote.objects.latest('id')
        self.assertEqual(vote.weight, 1)

        self.assertEqual(Vote.objects.count(), 1)


    def test_vote_2_times(self):
        response1 = self.client.post(self.vote_url, data=self.vote_data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.post(self.vote_url, data=self.vote_data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["message"], "Voted successfully")
        vote2 = Vote.objects.latest('id')
        self.assertEqual(vote2.weight, 0.5)

        self.assertEqual(Vote.objects.count(), 2)


    def test_vote_3_times(self):
        response1 = self.client.post(self.vote_url, data=self.vote_data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.post(self.vote_url, data=self.vote_data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        response3 = self.client.post(self.vote_url, data=self.vote_data)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data["message"], "Voted successfully")
        vote3 = Vote.objects.latest('id')
        self.assertEqual(vote3.weight, 0.25)


    def test_vote_on_a_not_existing_restaurant(self):
        vote_data = {
            "restaurant": 50
        }
        response = self.client.post(self.vote_url, data=vote_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_vote_with_no_data(self):
        vote_data = {}
        response = self.client.post(self.vote_url, data=vote_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"restaurant":["This field is required."]}')


    def test_vote_more_times_than_the_vote_limit(self):
        for i in range(0, vote_limit):
            self.client.post(self.vote_url, data=self.vote_data)

        response11 = self.client.post(self.vote_url, data=self.vote_data)
        self.assertEqual(response11.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response11.data["message"], f"Vote limit of {vote_limit} for this IP has been reached today")            
