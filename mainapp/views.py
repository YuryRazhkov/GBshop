import json
import os
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from mainapp.management.commands.fill import JSON_PATH
from mainapp.models import Product, ProductCategory


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
           }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'category': category_item,
            'products': products_paginator,

        }

        return render(request, 'mainapp/products_list.html', context)


    hot_product = get_hot_Product()

    context = {
        'links_menu': links_menu,
        'title': 'Продукты | Interior - online furniture shopping',
        'hot_product': hot_product,
        'same_products': get_same_product(hot_product),
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):

    with open(f"{settings.BASE_DIR}/contacts.json", encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты | Interior - online furniture shopping',
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
            'links_menu': links_menu,
            'product': get_object_or_404(Product, pk=pk),
               }
    return render(request, 'mainapp/product.html', context)


def main(request):
   title = 'главная'

   products = Product.objects.\
                      filter(is_active=True, category__is_active=True).\
                      select_related('category')[:3]

   content = {
       'title': title,
       'products': products,
   }
   return render(request, 'mainapp/index.html', content)


def load_from_json(file_name):
   with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
       return json.load(infile)
