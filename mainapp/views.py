from django.shortcuts import render
from django.conf import settings

from mainapp.models import Product

links_menu = [
    {'href': 'products', 'name': 'Все'},
    {'href': 'products_home', 'name': 'Дом'},
    {'href': 'products_modern', 'name': 'Модерн'},
    {'href': 'products_office', 'name': 'Офис'},
    {'href': 'products_classic', 'name': 'Классика'},
]


def index(request):

    product_list = Product.objects.all()
    print(product_list.query)

    context = {
        'titel': 'мой магазин',
        'products': product_list


    }

    return render(request, 'mainapp/index.html')

def products(request):
    context = {
        'links_menu': links_menu,
        'title': 'Все товары'
    }

    return render(request, 'mainapp/products.html', context)

def products_home(request):
    context = {
        'links_menu': links_menu,
        'title': 'Дом'
    }

    return render(request, 'mainapp/products.html', context)

def products_modern(request):
    context = {
        'links_menu': links_menu,
        'title': 'Модерн'
    }

    return render(request, 'mainapp/products.html', context)

def products_office(request):
    context = {
        'links_menu': links_menu,
        'title': 'Офис'
    }

    return render(request, 'mainapp/products.html', context)

def products_classic(request):
    context = {
        'links_menu': links_menu,
        'title': 'Классика'
    }

    return render(request, 'mainapp/products.html', context)

def contact(request):
    return render(request, 'mainapp/contact.html')
