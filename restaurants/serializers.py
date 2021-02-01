from rest_framework import serializers
from . models import Restaurant, Vote



class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ["name", "votes"]

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        exclude = ("id", "ip_address", "restaurant", "weight")