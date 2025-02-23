from django.shortcuts import render  , redirect 
from django.contrib.auth import authenticate , logout , login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def login_user(request):
    print("Login view called!") 
    if request.method == 'POST':
        print("POST request received")
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            return redirect('/')
        else:
            print("Login failed")
            messages.error(request, 'Invalid login credentials. Try again !!!!')
            return redirect(reverse('login_user'))

    print("Rendering login page")
    return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request , 'you are logged out')
    return redirect('/')



def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request ,'registarion successfull !!')
            return redirect('/')
    else:
        form = RegisterUserForm()  
    

    return render(request, 'authenticate/register_user.html', {'form': form})
