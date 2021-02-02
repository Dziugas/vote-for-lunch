from rest_framework import serializers
from . models import Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    todays_votes = serializers.DecimalField(max_digits=100000000, decimal_places=2, read_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "name", "todays_votes"]

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        exclude = ("id", "ip_address", "restaurant", "weight")