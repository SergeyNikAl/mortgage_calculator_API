from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

MIN_VALUE_TERM = 'Минимальный срок ипотеки не может быть менее 1 года'
MAX_VALUE_TERM = 'Максимальный срок ипотеки не должен превышать 30 лет'
VALUE_TERM_HELP = ('Введите срок ипотеки. Срок не может быть менее 1 года '
                   'и не может превышать 30 лет')
POSITIVE_VALUE_VALIDATION_MESSAGE = 'Поле должно быть более 0'

def validate_positive_value(value):
    if value <= 0:
        raise ValidationError(
            POSITIVE_VALUE_VALIDATION_MESSAGE
        )


class Offer(models.Model):
    bank_name = models.CharField(
        verbose_name='Нименование кредитного заведения',
        max_length=100
    )
    term_min = models.PositiveSmallIntegerField(
        'Срок ипотеки лет, ОТ',
        validators=(
            MinValueValidator(1, message=MIN_VALUE_TERM),
            MaxValueValidator(30, message=MAX_VALUE_TERM),
        ),
        help_text=VALUE_TERM_HELP
    )
    term_max = models.PositiveSmallIntegerField(
        'Срок ипотеки лет, ДО',
        validators=(
            MinValueValidator(1, message=MIN_VALUE_TERM),
            MaxValueValidator(30, message=MAX_VALUE_TERM),
        ),
        help_text=VALUE_TERM_HELP
    )
    rate_min = models.FloatField(
        'Ставка, ОТ',
        validators=[validate_positive_value]
    )
    rate_max = models.FloatField(
        'Ставка, ДО',
        validators=[validate_positive_value]
    )
    payment_min = models.PositiveIntegerField(
        'Сумма кредита, ОТ',
        validators=[validate_positive_value]
    )
    payment_max = models.PositiveIntegerField(
        'Сумма кредита, ДО',
        validators=[validate_positive_value]
    )


    class Meta:
        verbose_name = 'Предложения'
        verbose_name_plural = 'Предложения'

    def __str__(self):
        return self.bank_name
