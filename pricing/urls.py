from django.urls import path
from .views import CalculatePriceView


urlpatterns = [
    path('calc-price/', CalculatePriceView.as_view(), name="calc_price"),
]
