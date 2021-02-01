from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import Restaurant, Vote
from . serializers import RestaurantSerializer, VoteSerializer


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class VoteView(APIView):

    def post (self, request):

        serializer = VoteSerializer(data = request.data)
        if serializer.is_valid(raise_exception=ValueError):
            validated_data = request.data
            restaurant = get_object_or_404(Restaurant,
                                          id=validated_data["restaurant"])

            vote_ip_address = get_client_ip(request)
            todays_date = datetime.today()
            today_votes_from_same_ip = Vote.objects.filter(date=todays_date,
                                                      ip_address=vote_ip_address).count()
            vote_limit = 10
            if today_votes_from_same_ip == 0:
                score = 1
            elif today_votes_from_same_ip == 1:
                score = 0.5
            elif vote_limit > today_votes_from_same_ip > 1:
                score = 0.25
            elif today_votes_from_same_ip > vote_limit:
                return Response(
                    {
                        "message": f"Vote limit of {vote_limit} for this IP has been reached today"
                    }
                )

            Vote.objects.create(
                restaurant=restaurant,
                weight=score,
                ip_address = vote_ip_address
            )

            return Response(
                {
                    "message": "Voted successfully"
                },
                status=status.HTTP_200_OK
            )
