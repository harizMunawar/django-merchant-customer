from rest_framework import views
from core.serializers import CreateUserSerializer, MerchantSerializer, CustomerSerializer
from core.models import User, Merchant, Customer
from rest_framework.response import Response
from rest_framework import status

