from django.urls import include, path
from rest_framework import routers
from restaurants.views import RestaurantViewSet, VoteView, HistoryView

router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantViewSet)

app_name = "restaurants"
urlpatterns = [
    path('restaurant/<int:pk>/history/', HistoryView.as_view(), name='history'),
    path('', include(router.urls)),
    path('vote/', VoteView.as_view(), name='vote')
]

