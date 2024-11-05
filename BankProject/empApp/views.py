from django.shortcuts import render
from empApp.forms import EmployeeLoginForm

# Create your views here.
def emp_login(request):
    if request.method == "POST":
        form = EmployeeLoginForm(request.POST)
        pass
    else:
        form = EmployeeLoginForm()
        return render(request, 'empApp/emp-login.html', {'form': form, 'msg': 'Please Login to Continue'})
    

def mgr_login(request):
    if request.method == "POST":
        form = EmployeeLoginForm(request.POST)
        pass
    else:
        form = EmployeeLoginForm()
        return render(request, 'empApp/mgr-login.html', {'form': form, 'msg': 'Please Login to Continue'})
