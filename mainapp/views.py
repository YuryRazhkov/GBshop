from django.shortcuts import render

links_menu = [
    {'href': 'products', 'name': 'Все'},
    {'href': 'products_home', 'name': 'Дом'},
    {'href': 'products_modern', 'name': 'Модерн'},
    {'href': 'products_office', 'name': 'Офис'},
    {'href': 'products_classic', 'name': 'Классика'},
]


def index(request):
    return render(request, 'mainapp/index.html')

def products(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }

    return render(request, 'mainapp/products.html', context)

def products_home(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }

    return render(request, 'mainapp/products.html', context)

def products_modern(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }

    return render(request, 'mainapp/products.html', context)

def products_office(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }

    return render(request, 'mainapp/products.html', context)

def products_classic(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }

    return render(request, 'mainapp/products.html', context)

def contact(request):
    return render(request, 'mainapp/contact.html')
