
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'object_list': ShopUser.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/users_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):

        if request.method == 'POST':
            user_form = ShopUserRegisterForm(request.POST, request.FILES)
            if user_form.is_valid():
                user_form.save()
                return HttpResponseRedirect(reverse('adminapp:users'))
        else:
            user_form = ShopUserRegisterForm()

        context = {
            'form': user_form
        }
        return render(request, 'adminapp/users_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    curent_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=curent_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserAdminEditForm(instance=curent_user)

    context = {
        'form': user_form
    }
    return render(request, 'adminapp/users_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'object': current_user,
    }
    return render(request, 'adminapp/confirm_delete.html', context)




@user_passes_test(lambda u: u.is_superuser)
def categories(request):

    context = {

        'object_list': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/categories_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):


    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm()

    context = {
        'form': form
    }
    return render(request, 'adminapp/categories_forms.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm(instance=category_item)

    context = {
        'form': form
    }
    return render(request, 'adminapp/categories_forms.html', context)


@user_passes_test(lambda u: u.is_superuser)  # Попробывал реализовать удаление без формы подтверждения. Так правильно?
def category_delete(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    category_item.is_active = False
    category_item.save()
    context = {
        'object_list': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/categories_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'object_list': Product.objects.filter(category__pk=pk),
        'category': ProductCategory.objects.filter(id=pk),

    }
    return render(request, 'adminapp/product_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductForm()

    context = {
        'form': form
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    curent_item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=curent_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[curent_item.category.pk]))
    else:
        form = ProductForm(instance=curent_item)

    context = {
        'form': form
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    curent_item = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        curent_item.is_active = False
        curent_item.save()

        return HttpResponseRedirect(reverse('adminapp:products', args=[curent_item.category.pk]))

    context = {'object': curent_item}

    return render(request, 'adminapp/confirm_delete.html', context)





@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    pass



