from django.shortcuts import render
from django.conf import settings

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

    context = {
        'links_menu': links_menu,
        'title': 'Продукты | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/products.html', context)


def products_home(request):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'title': 'Дом'
    }

    return render(request, 'mainapp/products.html', context)

def products_modern(request):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'title': 'Модерн'
    }

    return render(request, 'mainapp/products.html', context)

def products_office(request):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'title': 'Офис'
    }

    return render(request, 'mainapp/products.html', context)

def products_classic(request):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'title': 'Классика'
    }

    return render(request, 'mainapp/products.html', context)

def contact(request):
    return render(request, 'mainapp/contact.html')
