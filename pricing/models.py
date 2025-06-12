from django.db import models

# Create your models here.

DAYS_OF_WEEK = [('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday'),]


class PricingConfig(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DistanceBasePrice(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='dbp')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_distance_km = models.FloatField()
    applicable_days = models.ManyToManyField('DayOfWeek')


class DistanceAdditionalPrice(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='dap')
    amount_per_km = models.DecimalField(max_digits=10, decimal_places=2)


class TimeMultiplier(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='tmf')
    min_minutes = models.IntegerField()
    max_minutes = models.IntegerField()
    multiplier = models.FloatField()


class WaitingCharge(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='wc')
    charge_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit_minutes = models.IntegerField()
    initial_free_minutes = models.IntegerField()


class PricingConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    actor = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


class DayOfWeek(models.Model):
    short_code = models.CharField(max_length=3, choices=DAYS_OF_WEEK, unique=True)

    def __str__(self):
        return self.get_short_code_display()

