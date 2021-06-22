from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import views
from rest_framework import permissions

from core.serializers import CreateUserSerializer, CustomerSerializer
from core.models import Customer, Merchant
from core.permissions import IsStaffOrReadOnly

from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

class CustomerList(views.APIView):
    permission_classes = [IsStaffOrReadOnly,]

    @swagger_auto_schema(
        responses={
            200: CustomerSerializer(),
            204: "No Content"
        }
    )
    def get(self, request):
        """
        Customer's List

        List all customers, if 0 customer exists return 204.
        """
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateUserSerializer(),
        responses={
            201: CustomerSerializer(),
            400: "Bad Request",
            403: "Staff Account is Required",
        }
    )
    def post(self, request):
        """
        Create Customer

        Username field must be unique.
        Return 201 with customer serializer if customer created successfully.
        Return 400 if request is invalid.
        Return 403 if request is done by a non-staff account.
        """
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_customer = True
            user.set_password(serializer.data["password"])
            user.save()
            
            customer = Customer.objects.get(id=user.customer.id)
            customer_serializer = CustomerSerializer(customer)
            return Response(customer_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated,]

    @swagger_auto_schema(
        responses={
            200: CustomerSerializer(),
            404: "Invalid Customer's ID or Not Found"
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Customer's Detail

        Return 200 with customer serializer if customer exists.
        Return 404 if no customer found with that ID.
        """
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CustomerSerializer(),
        responses={
            200: CustomerSerializer(),
            400: "Bad Request",
            403: "Either You Aren't Authenticated Or You Didn't Have Permission To Request",
            404: "Invalid Customer's ID or Not Found"
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Customer's Update

        Can only be done by an admin account or by requested account, return 403 otherwise.
        Return 200 with customer serializer if customer exists and updated successfully.
        Return 400 if request is invalid.
        Return 404 if no customer found with that ID.
        """

        if request.user.customer.id == kwargs["pk"] or request.user.is_superuser:
            return self.update(request, *args, **kwargs)
        return Response(
                {"detail": "Only Superuser or The Requested Account Can Perform This Action"},
                status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        responses={
            204: "No Content",
            403: "Either You Aren't Authenticated Or You Didn't Have Permission To Request",
            404: "Invalid Customer's ID or Not Found"
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Customer's Delete

        Can only be done by an admin account or by requested account, return 403 otherwise.
        Return 204 with no content if customer exists and deleted successfully.
        Return 404 if no customer found with that ID.
        """

        if request.user.customer.id == kwargs["pk"] or request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        return Response(
                {"detail": "Only Superuser or The Requested Account Can Perform This Action"},
                status=status.HTTP_403_FORBIDDEN)

class CustomerBuy(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]

    @swagger_auto_schema(
        responses={
            200: CustomerSerializer(),
            400: "Bad Request",
            402: "Customer Didn't Have Enough Balance To Complete The Transaction",
            403: "Only Authorized Customer Can Make A Transaction Using Their ID",
            404: "The Merchant ID Is Invalid, Thus Merchant Are Not Found"
        }
    )
    def post(self, request, merc_id, price):
        """
        Transaction

        Can only be done by a customer user, return 403 otherwise.
        Return 402 if customer doesn't have enough balance.
        Return 404 if no merchant with that ID exists.
        """
        if not request.user.is_customer:
            return Response(
                {"detail": "Only Authorized Customer Can Make A Transaction Using Their ID"},
                status=status.HTTP_403_FORBIDDEN)

        customer = get_object_or_404(Customer, id=request.user.customer.id)
        merchant = get_object_or_404(Merchant, id=merc_id)

        if customer.balance < price:
            return Response(
                {"detail": "Customer Did Not Have Enough Balance To Complete The Transaction"},
                status=status.HTTP_402_PAYMENT_REQUIRED)

        customer.balance -= price
        customer.save()

        merchant.balance += price
        merchant.save()

        return Response(
                {"detail": f"Transaction Successfull, Your Remaining Balance {customer.balance}"},
                status=status.HTTP_200_OK)