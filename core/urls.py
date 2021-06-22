from django.urls import path
from core import merchant_views, customer_views

urlpatterns = [
    path('merchants/', merchant_views.MerchantList.as_view()),
    path('merchants/<int:pk>/', merchant_views.MerchantDetail.as_view()),
    path('customers/', customer_views.CustomerList.as_view()),
    path('customers/<int:pk>/', customer_views.CustomerDetail.as_view()),
    path('transaction/<int:cust_id>/<int:merc_id>/<int:price>/', customer_views.CustomerBuy.as_view())
]
