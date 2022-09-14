from django.contrib import admin

from .models import Offer

EMPTY_VALUE = '-пусто-'

@admin.register(Offer)
class AdminOffer(admin.ModelAdmin):
    pass
