from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm
from django.contrib import messages
from .models import Account
from django.contrib.auth.decorators import login_required


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
            messages.success(request, f'Your account {email} has been created! Use your credential to login!')
            return redirect('account:login')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'account/profile.html', {})


@login_required
def update_profile(request):
    form = RegistrationForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('account:profile')

    return render(request, 'account/update_profile.html', {'form': form})
