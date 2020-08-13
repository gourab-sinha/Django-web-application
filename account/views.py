from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm
from django.contrib import messages
from .models import Account


def manager(request):
    context = {}
    return render(request, 'account/manager.html', context)


def user(request):
    context = {}
    return render(request, 'account/user.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been created! User your credential to login!')
            account_type = form.cleaned_data.get('account_type')
            return redirect('account:login')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def home(request):
    users = Account.objects.all()
    return render(request, 'account/home.html', {'users': users})