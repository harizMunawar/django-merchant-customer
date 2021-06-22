from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import views
from rest_framework import permissions

from core.serializers import CreateUserSerializer, MerchantSerializer
from core.models import Merchant
from core.permissions import IsStaffOrReadOnly

from drf_yasg.utils import swagger_auto_schema

class MerchantList(views.APIView):
    permission_classes = [IsStaffOrReadOnly,]

    @swagger_auto_schema(
        responses={
            200: MerchantSerializer(),
            204: "No Content"
        }
    )
    def get(self, request):
        """
        Merchant's List

        List all merchants, if 0 merchant exists return 204.
        """
        merchant = Merchant.objects.all()
        serializer = MerchantSerializer(merchant, many=True)
        if not serializer.data:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateUserSerializer(),
        responses={
            201: MerchantSerializer(),
            400: "Bad Request",
            403: "Staff Account is Required",
        }
    )
    def post(self, request):
        """
        Create Merchant

        Username field must be unique.
        Return 201 with merchant serializer if merchant created successfully.
        Return 400 if request is invalid.
        Return 403 if request is done by a non-staff account.
        """
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_merchant = True
            user.set_password(serializer.data["password"])
            user.save()

            merchant = Merchant.objects.get(id=user.merchant.id)
            merchant_serializer = MerchantSerializer(merchant)
            return Response(merchant_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MerchantDetail(
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated,]

    @swagger_auto_schema(
        responses={
            200: MerchantSerializer(),
            404: "Invalid Merchant's ID or Not Found"
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Merchant's Detail

        Return 200 with merchant serializer if merchant exists.
        Return 404 if no merchant found with that ID.
        """
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=MerchantSerializer(),
        responses={
            200: MerchantSerializer(),
            400: "Bad Request",
            403: "Either You Aren't Authenticated Or You Didn't Have Permission To Request",
            404: "Invalid Merchant's ID or Not Found"
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Merchant's Update

        Can only be done by an admin account or by requested account, return 403 otherwise.
        Return 200 with merchant serializer if merchant exists and updated successfully.
        Return 400 if request is invalid.
        Return 404 if no merchant found with that ID.
        """

        if request.user.merchant.id == kwargs["pk"] or request.user.is_superuser:
            return self.update(request, *args, **kwargs)
        return Response(
                {"detail": "Only Superuser or The Requested Account Can Perform This Action"},
                status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        responses={
            204: "No Content",
            403: "Either You Aren't Authenticated Or You Didn't Have Permission To Request",
            404: "Invalid Merchant's ID or Not Found"
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Merchant's Delete

        Can only be done by an admin account or by requested account, return 403 otherwise.
        Return 204 with no content if merchant exists and deleted successfully.
        Return 404 if no merchant found with that ID.
        """

        if request.user.merchant.id == kwargs["pk"] or request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        return Response(
                {"detail": "Only Superuser or The Requested Account Can Perform This Action"},
                status=status.HTTP_403_FORBIDDEN)
