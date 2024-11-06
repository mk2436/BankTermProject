from django.shortcuts import render
from empApp.decorators import role_required
from empApp.models import Employee
# Create your views here.

def home(request):
    return render(request, 'rootApp/home.html')

@role_required('manager', 'assistanMgr', 'employee', 'customer', login_url='')
def user_profile(request):
    username = request.user.username
    try:
        if request.user.user_type == "customer":
            id = request.user.customerid
        else:
            employee = Employee.objects.get(empid=username)
            name = employee.name
            id = employee.empid
            bid = employee.bid.bid
        data = {'name':name, 'id': id, 'bid':bid}
        return render(request, 'rootApp/user-profile.html', {'data':data})
    except Employee.DoesNotExist:
        return render(request, 'rootApp/user-profile.html', {'name':'Not Available', 'ID': 'Not Available'})
    