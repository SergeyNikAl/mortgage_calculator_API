from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from mortgage.models import Offer
from .serializers import (
    OfferCreateSerializer,
    OfferSerializer,
)

from .filters import OfferFilter


class OfferViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_class = OfferFilter

    def get_queryset(self):
        queryset = Offer.objects.all()
        price = self.request.query_params.get('price')
        if price:
            queryset = queryset.filter(payment_max__lte=price,)
        return queryset

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return OfferSerializer
        return OfferCreateSerializer
