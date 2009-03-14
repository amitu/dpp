from django.contrib import admin

from dpp.models import PaymentRequest

admin.site.register(PaymentRequest, admin.ModelAdmin)
