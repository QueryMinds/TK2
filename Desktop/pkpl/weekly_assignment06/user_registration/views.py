from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Normally we would save to database here
            # For demo purposes, we're just passing the clean data to the template
            validated_data = form.cleaned_data
            return render(request, 'user_registration/success.html', {'data': validated_data})
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user_registration/register.html', {'form': form})

def success(request):
    return render(request, 'user_registration/success.html')