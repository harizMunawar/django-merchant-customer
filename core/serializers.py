from rest_framework import serializers
from core.models import User, Merchant, Customer

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class MerchantSerializer(serializers.ModelSerializer):
    user =  serializers.SerializerMethodField()

    def get_user(self, merchant):
        qs = User.objects.get(id=merchant.user.id)
        return SafeUserSerializer(instance=qs).data

    class Meta:
        model = Merchant
        fields = ("id", "user", "balance")

class CustomerSerializer(serializers.ModelSerializer):
    user =  serializers.SerializerMethodField()

    def get_user(self, merchant):
        qs = User.objects.get(id=merchant.user.id)
        return SafeUserSerializer(instance=qs).data

    class Meta:
        model = Customer
        fields = ("id", "user", "balance")
