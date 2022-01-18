from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product

# from django.contrib.auth.models import User
from authapp.models import ShopUser as User, ShopUser, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
       for user in ShopUser.objects.all():
           ShopUserProfile.objects.create(user=user)
