from rest_framework import serializers, status

from mortgage.models import Offer

MONTHS_IN_YEAR = 12
TO_PERCENT = 100
ERROR_LOAN = 'Сумма кредита должна быть больше 0'
EMPTY_BANK_NAME = 'Необходимо указать имя банка'
EMPTY_PARAMETER = 'Необходимо заполнить поля "{value}"'


class OfferSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения предложений с учетом расчета стоимости
    """
    payment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Offer
        fields = (
            'id',
            'bank_name',
            'term_min',
            'term_max',
            'rate_min',
            'rate_max',
            'payment_min',
            'payment_max',
            'payment',
        )

    def _calculate_payment(self, instance):
        """
        Расчет ежемесячного платежа
        """
        price = int(self.context.get('request').query_params.get('price'))
        deposit = int(self.context.get('request').query_params.get('deposit'))
        term = int(self.context.get('request').query_params.get('term'))
        loan = price - deposit
        if loan <= 0:
            raise serializers.ValidationError(ERROR_LOAN)
        monthly_percent = instance.rate_min / MONTHS_IN_YEAR / TO_PERCENT
        mortgage_months = term * MONTHS_IN_YEAR
        payment = int((loan * monthly_percent) / (1 - (
                1 + monthly_percent
        ) ** (-mortgage_months)))
        return payment

    def get_payment(self, obj):
        """
        Отображение ежемесячного платежа при выводе списка предложений
        """
        try:
            request = self.context.get('request')
            price = request.query_params.get('price', 0)
            deposit = request.query_params.get('deposit', 0)
            term = request.query_params.get('term', 0)
            if request.method in ('GET', 'PATCH'):
                if any([not price, not deposit, not term]):
                    return None
                if any([price == 0, deposit == 0, term == 0]):
                    return None
                return self._calculate_payment(obj)
        except (ValueError, TypeError):
            return None

class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания предложений
    """

    class Meta:
        model = Offer
        fields = '__all__'

    def validate(self, data):
        bank_name = data.get('bank_name')
        invalid_data = []
        new_data = {
            'term_min': data.get('term_min'),
            'term_max': data.get('term_max'),
            'rate_min': data.get('rate_min'),
            'rate_max': data.get('rate_max'),
            'payment_min': data.get('payment_min'),
            'payment_max': data.get('payment_max'),
        }
        if not bank_name:
            raise serializers.ValidationError(EMPTY_BANK_NAME)
        for parameter, value in new_data.items():
            if not value:
                invalid_data.append(parameter)
        if invalid_data:
            raise serializers.ValidationError(
                EMPTY_PARAMETER.format(value=', '.join(invalid_data))
            )
        return data

    def create(self, validated_data):
        """
        Метод создания предложения
        """
        offer, _ = Offer.objects.get_or_create(**validated_data)
        return offer

    def update(self, instance, validated_data):
        """
        Метод для обновления предложения.
        """
        instance.bank_name = validated_data.get(
            'bank_name', instance.bank_name
        )
        instance.term_min = validated_data.get('term_min', instance.term_min)
        instance.term_max = validated_data.get('term_max', instance.term_max)
        instance.rate_min = validated_data.get('rate_min', instance.rate_min)
        instance.rate_max = validated_data.get('rate_max', instance.rate_max)
        instance.payment_min = validated_data.get(
            'payment_min', instance.payment_min
        )
        instance.payment_max = validated_data.get(
            'payment_max', instance.payment_max
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Отображение объектов в соответствии с запросом
        """
        return OfferSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
