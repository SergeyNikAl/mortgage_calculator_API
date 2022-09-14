from rest_framework.routers import DefaultRouter

from api.views import OfferViewSet

name = 'api'

router_v1 = DefaultRouter()
router_v1.register('offer', OfferViewSet, basename='offer')

