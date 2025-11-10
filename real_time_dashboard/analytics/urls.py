from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='analytics_dashboard'),
    path('stock_price/', views.stock_price, name='stock_price_api'),
]