import json

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def index(request):

    products_list = Product.objects.all()[:4]
    print(products_list.query)

    context = {
        'title': 'Главная | Interior - online furniture shopping',
        'products': products_list
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
            'basket': Basket.objects.filter(user=request.user),
        }

        return render(request, 'mainapp/products_list.html', context)


    context = {
        'links_menu': links_menu,
        'title': 'Продукты | Interior - online furniture shopping',
        'hot_product': Product.objects.all().first(),
        'same_products': Product.objects.all()[3:5],
        'basket': Basket.objects.filter(user=request.user),


    }
    return render(request, 'mainapp/products.html', context)


def contact(request):

    with open(f"{settings.BASE_DIR}/contacts.json", encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты | Interior - online furniture shopping'
        }
    return render(request, 'mainapp/contact.html', context)
