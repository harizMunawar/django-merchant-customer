from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import views

from core.serializers import CreateUserSerializer, CustomerSerializer
from core.models import Customer
from core.permissions import IsStaffOrReadOnly

from drf_yasg.utils import swagger_auto_schema

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
    permission_classes = [IsStaffOrReadOnly,]

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
            404: "Invalid Customer's ID or Not Found"
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Customer's Update

        Return 200 with customer serializer if customer exists and updated successfully.
        Return 400 if request is invalid.
        Return 404 if no customer found with that ID.
        """
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: "No Content",
            404: "Invalid Customer's ID or Not Found"
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Customer's Delete

        Return 204 with no content if customer exists and deleted successfully.
        Return 404 if no customer found with that ID.
        """
        return self.destroy(request, *args, **kwargs)