import django_filters as filters

from mortgage.models import Offer


class OfferFilter(filters.FilterSet):
    rate_min = filters.NumberFilter(lookup_expr='gte',)
    rate_max = filters.NumberFilter(lookup_expr='lte',)
    payment_min = filters.NumberFilter(lookup_expr='gte',)
    payment_max = filters.NumberFilter(lookup_expr='lte',)

    class Meta:
        model = Offer
        fields = (
            'rate_min',
            'rate_max',
            'payment_min',
            'payment_max'
        )