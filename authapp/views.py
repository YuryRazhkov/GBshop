from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileForm
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from authapp.models import ShopUser


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
        edit_profile_form = ShopUserProfileForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))

    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = ShopUserProfileForm(instance=request.user.shopuserprofile)

    context = {
        'edit_form': edit_form,
        'edit_profile_form': edit_profile_form,
    }

    return render(request, 'authapp/edit.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
            return HttpResponseRedirect(reverse('authapp:login'))

    else:
        register_form = ShopUserRegisterForm()

    context = {
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', context)

def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            print("user_is:", user, activation_key, user.activation_key, user.activation_key_expired)
            user.is_activate = True
            user.activation_key = None
            user.activation_key_expired = None
            user.save()
            auth.login(request, user)
    return render(request, 'authapp/verify.html')

def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])

    subject = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.BASE_URL} перейдите по ссылке: \n{settings.BASE_URL}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)