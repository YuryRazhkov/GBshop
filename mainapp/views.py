import json
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []

def get_hot_Product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]

def get_same_product(hot_product):
    same_product_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_product_list[:3]


def index(request):

    products_list = Product.objects.all()[:4]


    context = {
        'title': 'Главная | Interior - online furniture shopping',
        'products': products_list,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        context = {
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
            'basket': get_basket(request.user),
        }

        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_hot_Product()

    context = {
        'links_menu': links_menu,
        'title': 'Продукты | Interior - online furniture shopping',
        'hot_product': hot_product,
        'same_products': get_same_product(hot_product),
        'basket': get_basket(request.user),


    }
    return render(request, 'mainapp/products.html', context)


def contact(request):

    with open(f"{settings.BASE_DIR}/contacts.json", encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты | Interior - online furniture shopping',
            'basket': get_basket(request.user),
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
            'links_menu': links_menu,
            'product': get_object_or_404(Product, pk=pk),
            'basket': get_basket(request.user),
        }
    return render(request, 'mainapp/product.html', context)
