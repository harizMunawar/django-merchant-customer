from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def create_user(self, username, is_merchant, is_customer, password=None, **kwargs):
        if not username:
            raise ValueError("Data is not complete")

        if (not is_merchant and not is_customer) or (is_merchant and is_customer) or kwargs["is_superuser"]:
            raise ValidationError("A user must either be merchant or customer or a superuser")

        user = self.model(username=username, is_merchant=is_merchant, is_customer=is_customer, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, is_merchant, is_customer, password):
        user = self.create_user(username=username, is_merchant=is_merchant, is_customer=is_customer, password=password, is_superuser=True)
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    is_merchant = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["is_merchant", "is_customer"]

    objects = UserManager()
    
    def __str__(self):
        return self.username or ""

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

class Merchant(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="merchant", default=None)
    balance = models.IntegerField()

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="customer", default=None)
    balance = models.IntegerField()

    def __str__(self):
        return self.user.username

@receiver(models.signals.post_save, sender=User)
def auto_create_extended_object(sender, instance, created, **kwargs):
    if instance.is_merchant:
        merc, created = Merchant.objects.get_or_create(user=instance, defaults={
            'balance': 0,
        })

    if instance.is_customer:
        Customer.objects.get_or_create(user=instance, defaults={
            'balance': 0,
        })

@receiver(models.signals.post_delete, sender=Merchant)
def auto_delete_user(sender, instance, **kwargs):
    User.objects.get(id=instance.user.id).delete()

@receiver(models.signals.post_delete, sender=Customer)
def auto_delete_user2(sender, instance, **kwargs):
    User.objects.get(id=instance.user.id).delete()
