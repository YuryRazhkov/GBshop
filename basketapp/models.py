from functools import cached_property

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from mainapp.models import Product

#
# class BasketQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super().delete(*args, **kwargs)
from ordersapp.models import OrderItem


class Basket(models.Model):
    # object = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    # @property
    def product_cost(self):
        return self.product.price * self.quantity

    product_cost = property(product_cost)



    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    #
    # @property
    # def total_quantity(self):
    #     items = Basket.objects.filter(user=self.user)
    #     _total_quantity = sum(list(map(lambda x: x.quantity, items)))
    #     return _total_quantity
    #
    #
    # @property
    # def total_cost(self):
    #     items = Basket.objects.filter(user=self.user)
    #     _total_cost = sum(list(map(lambda x: x.product_cost, items)))
    #     return _total_cost

    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)


