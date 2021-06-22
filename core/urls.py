from django.urls import path
from core import views, merchant_views, customer_views

urlpatterns = [
    path('merchants/', merchant_views.MerchantList.as_view()),
    path('merchants/<int:id>/', merchant_views.MerchantDetail.as_view()),
    path('customers/', customer_views.CustomerList.as_view()),
    path('customers/<int:id>/', customer_views.CustomerDetail.as_view()),
]
