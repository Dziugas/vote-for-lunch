from django.urls import include, path
from rest_framework import routers
from restaurants.views import RestaurantViewSet, VoteView

router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantViewSet)

app_name = "restaurants"
urlpatterns = [
    path('', include(router.urls)),
    path('vote/', VoteView.as_view(), name='vote')
]

