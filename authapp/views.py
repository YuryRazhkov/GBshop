from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


def login(request):
    title = 'вход'
    next_url = request.GET.get('next', '')
    login_form = ShopUserLoginForm(data=request.POST)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))

    context = {'title': title,
               'login_form': login_form,
               'next': next_url,
               }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))

    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {
        'edit_form': edit_form
    }

    return render(request, 'authapp/edit.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))

    else:
        register_form = ShopUserRegisterForm()

    context = {
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', context)

def verify(request, email, acctivation_key):
    pass

def send_verify_mail(user):
    verify_link = "reverse('auth:verify', args=[user.email, user.activation_key])"
   
    subject = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.BASE_URL} перейдите по ссылке: \n{settings.BASE_URL}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)