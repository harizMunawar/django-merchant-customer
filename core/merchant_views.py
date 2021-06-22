from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import views

from core.serializers import CreateUserSerializer, MerchantSerializer
from core.models import Merchant
from core.permissions import IsStaffOrReadOnly


class MerchantList(views.APIView):
    """
    List all merchants or create a new one
    """

    permission_classes = [IsStaffOrReadOnly,]

    def get(self, request):
        merchant = Merchant.objects.all()
        serializer = MerchantSerializer(merchant, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_merchant = True
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

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)