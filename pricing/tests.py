from django.test import TestCase
from .models import PricingConfig, DistanceBasePrice, DistanceAdditionalPrice, TimeMultiplier, WaitingCharge, DayOfWeek
from decimal import Decimal

from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

class PricingConfigTestCase(TestCase):
    def setUp(self):
        # Set up necessary data for testing
        monday = DayOfWeek.objects.create(short_code="Mon")
        tuesday = DayOfWeek.objects.create(short_code="Tue")
        self.config = PricingConfig.objects.create(name="Standard Pricing", is_active=True)

        # Create associated model entries
        self.dbp = DistanceBasePrice.objects.create(
            config=self.config,
            amount=80.0,
            max_distance_km=3.0,
        )

        self.dbp.applicable_days.add(monday)
        self.dbp.save()

        self.dap = DistanceAdditionalPrice.objects.create(
            config=self.config,
            amount_per_km=30.0,
        )

        self.tmf = TimeMultiplier.objects.create(
            config=self.config,
            min_minutes=0,
            max_minutes=60,
            multiplier=1.0
        )

        self.wc = WaitingCharge.objects.create(
            config=self.config,
            charge_per_unit=5.0,
            unit_minutes=3,
            initial_free_minutes=3
        )

    def test_pricing_config_creation(self):
        # Test that PricingConfig is created
        self.assertEqual(self.config.name, "Standard Pricing")
        self.assertTrue(self.config.is_active)

    def test_dbp_creation(self):
        # Test that DistanceBasePrice is created
        self.assertEqual(self.dbp.amount, 80.0)
        self.assertEqual(self.dbp.max_distance_km, 3.0)

    def test_dap_creation(self):
        # Test that DistanceAdditionalPrice is created
        self.assertEqual(self.dap.amount_per_km, 30.0)

    def test_tmf_creation(self):
        # Test that TimeMultiplier is created
        self.assertEqual(self.tmf.multiplier, 1.0)

    def test_wc_creation(self):
        # Test that WaitingCharge is created
        self.assertEqual(self.wc.charge_per_unit, 5.0)
        self.assertEqual(self.wc.unit_minutes, 3)

    def test_price_calculation_logic(self):
        # Test the price calculation logic with basic assertions
        from .utils import calculate_price

        calculated_price = calculate_price(distance=5.5, ride_time=55, waiting_time=6, day_str="Mon")
        self.assertEqual(calculated_price, 215.0)


class CalculatePriceAPITestCase(APITestCase):
    def setUp(self):
        # Set up necessary data for testing
        monday = DayOfWeek.objects.create(short_code="Mon")
        tuesday = DayOfWeek.objects.create(short_code="Tue")
        self.config = PricingConfig.objects.create(name="Standard Pricing", is_active=True)

        # Create associated model entries
        self.dbp = DistanceBasePrice.objects.create(
            config=self.config,
            amount=80.0,
            max_distance_km=3.0,
        )

        self.dbp.applicable_days.add(monday)
        self.dbp.save()

        self.dap = DistanceAdditionalPrice.objects.create(
            config=self.config,
            amount_per_km=30.0,
        )

        self.tmf = TimeMultiplier.objects.create(
            config=self.config,
            min_minutes=0,
            max_minutes=60,
            multiplier=1.0
        )

        self.wc = WaitingCharge.objects.create(
            config=self.config,
            charge_per_unit=5.0,
            unit_minutes=3,
            initial_free_minutes=3
        )

    def test_calculate_price_valid_data(self):
        url = '/api/calc-price/'

        data = {
            "distance": 4.5,
            "ride_time": 45,
            "waiting_time": 3,
            "day_str": "Mon"
        }

        response = self.client.post(url, data, format='json')

        # Ensure status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure price is calculated correctly in the response
        self.assertEqual(response.data['price'], 170.0)

    def test_calculate_price_invalid_day(self):
        url = '/api/calc-price/'

        data = {
            "distance": 4.5,
            "ride_time": 45,
            "waiting_time": 3,
            "day_str": "Fri"  # Invalid day
        }

        response = self.client.post(url, data, format='json')

        # Ensure status code is 400 Bad Request due to invalid day
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check for error message
        self.assertIn('Invalid day', response.data['error'])
        self.assertTrue(
            'Invalid day' in response.data['error'] or
            'No DBP rule found' in response.data['error']
        )

        # self.assertIn('No active pricing config found', response.data['error'])

    def test_calculate_price_missing_field(self):
        url = '/api/calc-price/'

        data = {
            "distance": 4.5,
            "ride_time": 45,
            # Missing "waiting_time"
            "day_str": "Mon"
        }

        response = self.client.post(url, data, format='json')

        # Ensure status code is 400 Bad Request due to missing field
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
