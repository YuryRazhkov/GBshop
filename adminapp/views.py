from django.shortcuts import render

from authapp.models import ShopUser
from mainapp.models import Product


def users(request):
    context = {
        'object_list': ShopUser.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/users_list.html', context)

def user_create(request):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)

def user_update(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)


def user_delete(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)


def categories(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)


def product(request, pk):
    context = {
        'object_list': Product.objects.all()
    }
    return render(request, 'adminapp/categories_list.html', context)


def category_create(request):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)


def category_update(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)


def category_delete(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)

def products(request, pk):
    context = {
        'object_list': Product.objects.filter(category_pk=pk)

    }
    return render(request, 'adminapp/product_list.html', context)


def product_create(request):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)


def product_update(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)


def product_delete(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)

def product_read(request, pk):
    context = {

    }
    return render(request, 'adminapp/users_list.html', context)



