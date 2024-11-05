from django.shortcuts import render

# Create your views here.
def emp_login(request):
    return render(request, 'emp-login.html')