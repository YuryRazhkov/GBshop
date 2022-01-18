
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
# from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
# from django.views.generic.edit import BaseDeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/users_list.html', context)




class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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

#
# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#
#
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'adminapp/categories_forms.html', context)

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/categories_forms.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

#
# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST, instance=category_item)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryForm(instance=category_item)
#
#     context = {
#         'form': form
#     }
#     return render(request, 'adminapp/categories_forms.html', context)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/categories_forms.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')




# @user_passes_test(lambda u: u.is_superuser)  # Попробывал реализовать удаление без формы подтверждения. Так правильно?
# def category_delete(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     category_item.is_active = False
#     category_item.save()
#     context = {
#         'object_list': ProductCategory.objects.all()
#     }
#     return render(request, 'adminapp/categories_list.html', context)

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/confirm_delete.html'
    success_url = reverse_lazy('adminapp:categories')


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     context = {
#         'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active'),
#         'category': ProductCategory.objects.filter(id=pk),
#
#     }
#     return render(request, 'adminapp/product_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    context = {
        'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active'),
        'category': get_object_or_404(ProductCategory, pk=pk),
    }

    return render(request, 'adminapp/product_list.html', context)



# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product_item = form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
#     else:
#         form = ProductForm()
#
#     context = {
#         'form': form,
#         'category': category_item
#     }
#     return render(request, 'adminapp/product_form.html', context)

class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('adminapp:categories')



    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print('context_data', context_data)
        category_id = self.kwargs.get('pk')
        print('category_id', category_id)
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        # category_item = get_object_or_404(Product, pk=category_id)
        print('category_item', category_item)

        context_data['category'] = category_item
        print('category_item', category_item)
        print('context_data', context_data)
        return context_data

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.kwargs.get('pk')])

       # product_id = self.kwargs.get('pk')
       #  product = get_object_or_404(Product, pk=product_id)
       #  return reverse_lazy('adminapp:products', args=[product.category.pk])

# def product_create(request, pk):
#     title = 'продукт/создание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductForm(initial={'category': category})
#
#     content = {'title': title,
#                'update_form': product_form,
#                'category': category
#                }
#
#     return render(request, 'adminapp/confirm_delete.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     curent_item = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=curent_item)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[curent_item.category_id]))
#     else:
#         form = ProductForm(instance=curent_item)
#
#     context = {
#         'object': curent_item,
#         'form': form,
#     }
#     return render(request, 'adminapp/product_form.html', context)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    # fields = '__all__'
    form_class = ProductForm



    def get_success_url(self):
        product_id = self.kwargs.get('pk')
        print('product_id', product_id)
        product = get_object_or_404(Product, pk=product_id)
        print('product', product)
        return reverse_lazy('adminapp:products', args=[product.category.pk])


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    curent_item = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        curent_item.is_active = False
        curent_item.save()

        return HttpResponseRedirect(reverse('adminapp:products', args=[curent_item.category.pk]))

    context = {'object': curent_item}

    return render(request, 'adminapp/confirm_delete.html', context)



#
# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     curent_item = get_object_or_404(Product, pk=pk)
#
#     context = {'object': curent_item}
#
#     return render(request, 'adminapp/product_read.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

