from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm
from django.contrib import messages


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
            messages.success(request, f'Account created for {email}!')
            account_type = form.cleaned_data.get('account_type')
            if account_type == "MANAGER":
                return redirect('account:manager')
            else:
                return redirect('account:user')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})
