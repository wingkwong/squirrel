from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.dob = form.cleaned_data.get('dob')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('tracker:expense')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')