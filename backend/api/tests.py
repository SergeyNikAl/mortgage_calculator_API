from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .views import OfferViewSet
from mortgage.models import Offer


class TestOfferClass(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.offer_1 = Offer.objects.create(
            id=1,
            bank_name='bank_test_1',
            term_min=1,
            term_max=30,
            rate_min=7.9,
            rate_max=11.9,
            payment_min=300000,
            payment_max=500000
        )
        cls.offer_2 = Offer.objects.create(
            id=2,
            bank_name='bank_test_2',
            term_min=10,
            term_max=30,
            rate_min=11.7,
            rate_max=23.4,
            payment_min=1000000,
            payment_max=10000000
        )
        cls.offer_3 = Offer.objects.create(
            id=3,
            bank_name='bank_test_3',
            term_min=10,
            term_max=40,
            rate_min=1.6,
            rate_max=2,
            payment_min=1000000,
            payment_max=10000000
        )

    def test_create_offer(self):
        """
        Предложение сформировано с корректным контекстом
        """
        data = {
            'id': 4,
            'bank_name': 'bank_test_4',
            'term_min': 10,
            'term_max': 30,
            'rate_min': 7.9,
            'rate_max': 11.9,
            'payment_min': 1000000,
            'payment_max': 10000000
        }
        factory = APIRequestFactory()
        request = factory.post('/api/offer/', data)
        view = OfferViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(Offer.objects.count(), 4)
        self.assertEqual(response.data['bank_name'], 'bank_test_4')
        self.assertEqual(response.data['term_min'], 10)
        self.assertEqual(response.data['term_max'], 30)
        self.assertEqual(response.data['rate_min'], 7.9)
        self.assertEqual(response.data['rate_max'], 11.9)
        self.assertEqual(response.data['payment_min'], 1000000)
        self.assertEqual(response.data['payment_max'], 10000000)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_offer(self):
        data = {
            'id': 4,
            'bank_name': 'bank_test_4',
            'term_min': 3,
            'term_max': 15,
            'rate_min': 6.9,
            'rate_max': 12.9,
            'payment_min': 1100000,
            'payment_max': 11000000
        }
        factory = APIRequestFactory()
        request = factory.patch('/api/offer/', data)
        view = OfferViewSet.as_view({'patch': 'update'})
        response = view(request, pk=self.data.get('id'))
        self.assertEqual(Offer.objects.count(), 4)
        self.assertEqual(response.data['bank_name'], 'bank_test_4')
        self.assertEqual(response.data['term_min'], 3)
        self.assertEqual(response.data['term_max'], 15)
        self.assertEqual(response.data['rate_min'], 6.9)
        self.assertEqual(response.data['rate_max'], 12.9)
        self.assertEqual(response.data['payment_min'], 1100000)
        self.assertEqual(response.data['payment_max'], 11000000)

    def test_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/offer/')
        view = OfferViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
