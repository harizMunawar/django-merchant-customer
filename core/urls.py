from django.urls import path
from core import views, merchant_views, customer_views

urlpatterns = [
    path('merchants/', merchant_views.MerchantList.as_view()),
    path('merchants/<int:pk>/', merchant_views.MerchantDetail.as_view()),
    path('customers/', customer_views.CustomerList.as_view()),
    path('customers/<int:pk>/', customer_views.CustomerDetail.as_view()),
]
