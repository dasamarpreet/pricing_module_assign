from .models import PricingConfig, DayOfWeek
from datetime import datetime
from decimal import Decimal


def calculate_price(distance: float, ride_time: float, waiting_time: float, day_str: str) -> float:
    config = PricingConfig.objects.filter(is_active=True).first()
    if not config:
        raise Exception("No active pricing config found")

    # Get the right DBP for the day
    try:
        day_obj = DayOfWeek.objects.get(short_code=day_str)
        dbp_rule = config.dbp.filter(applicable_days=day_obj).first()
        if not dbp_rule:
            raise Exception(f"No DBP rule found for day: {day_str}")
    except DayOfWeek.DoesNotExist:
        raise Exception(f"Invalid day: {day_str}")

    # Distance cost
    base_price = dbp_rule.amount
    base_distance = dbp_rule.max_distance_km
    extra_distance = max(Decimal(distance) - Decimal(base_distance), Decimal(0))

    dap = config.dap.first()
    if not dap:
        raise Exception("No Distance Additional Price (DAP) rule found")

    extra_distance_cost = Decimal(extra_distance) * Decimal(dap.amount_per_km)

    # Time cost
    tmf_rule = config.tmf.filter(min_minutes__lte=ride_time, max_minutes__gte=ride_time).first()
    if not tmf_rule:
        raise Exception("No TMF rule matched for this ride time")

    time_cost = Decimal(ride_time) * Decimal(tmf_rule.multiplier)

    # Waiting cost
    wc_rule = config.wc.first()
    if not wc_rule:
        raise Exception("No Waiting Charge rule found")

    chargeable_wait = max(waiting_time - wc_rule.initial_free_minutes, 0)
    waiting_blocks = chargeable_wait // wc_rule.unit_minutes
    waiting_cost = Decimal(waiting_blocks) * Decimal(wc_rule.charge_per_unit)

    total = Decimal(base_price) + Decimal(extra_distance_cost) + Decimal(time_cost) + Decimal(waiting_cost)
    return float(round(total, 2))
