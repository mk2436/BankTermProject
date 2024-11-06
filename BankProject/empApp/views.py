from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from empApp.forms import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def emp_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            employee = authenticate(request, username=username, password=password)
            if employee is not None:
                login(request,employee)
                return redirect('home')
    else:
        form = LoginForm()
        return render(request, 'empApp/emp-login.html', {'form': form, 'msg': 'Please Login to Continue'})
    
@login_required(login_url='emp-login')
def emp_logout(request):
    logout(request)
    return redirect('emp-login')

def mgr_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            manager = authenticate(request, username=username)
    else:
        form = LoginForm()
        return render(request, 'empApp/mgr-login.html', {'form': form, 'msg': 'Please Login to Continue'})
