from django.contrib import admin
from .models import PricingConfig, DistanceBasePrice, DistanceAdditionalPrice, TimeMultiplier, WaitingCharge, PricingConfigLog, DayOfWeek


class DistanceBasePriceInline(admin.TabularInline):
    model = DistanceBasePrice
    extra = 1
    filter_horizontal = ('applicable_days',)

class DistanceAdditionalPriceInline(admin.TabularInline):
    model = DistanceAdditionalPrice
    extra = 1

class TimeMultiplierInline(admin.TabularInline):
    model = TimeMultiplier
    extra = 1

class WaitingChargeInline(admin.TabularInline):
    model = WaitingCharge
    extra = 1

@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    inlines = [
        DistanceBasePriceInline,
        DistanceAdditionalPriceInline,
        TimeMultiplierInline,
        WaitingChargeInline,
    ]
    list_display = ('name', 'is_active', 'created_at')

    def save_model(self, request, obj, form, change):
        action = "Updated" if change else "Created"
        super().save_model(request, obj, form, change)
        PricingConfigLog.objects.create(
            config=obj,
            action=action,
            actor=request.user.username
        )

@admin.register(PricingConfigLog)
class PricingConfigLogAdmin(admin.ModelAdmin):
    list_display = ('config', 'action', 'actor', 'timestamp')

admin.site.register(DayOfWeek)
