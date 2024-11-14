from django.shortcuts import render
from empApp.decorators import role_required
from empApp.models import Employee, Customer, PersonalBanker, Manager
# Create your views here.

def home(request):
    return render(request, 'rootApp/home.html')

@role_required('manager', 'assistanMgr', 'employee', 'customer', login_url='/')
def user_profile(request):
    username = request.user.username
    try:
        if request.user.user_type == "customer":
            customer = Customer.objects.get(customerid=username)
            id = customer.customerid
            name = customer.name
            personalBanker = PersonalBanker.objects.get(customerid=id)
            bid = personalBanker.empid.bid.bid
            data = {'name':name, 'id': id}
            branch = {}
            banker = {'name':personalBanker.empid.name, 'teleno': personalBanker.empid.teleno,'bid':bid}
        elif request.user.user_type in ("manager", "assistanMgr") :
            employee = Employee.objects.get(empid=username)
            name = employee.name
            id = employee.empid
            bid = employee.bid.bid
            data = {'name':name, 'id': id, 'bid':bid}

            branch = Manager.objects.get(manager=employee.ssn)
            branch = {'name': branch.bid.name, 'city':branch.bid.city, 'address': branch.bid.address, 'id': branch.bid.bid}
            banker = {}
            
        else:
            employee = Employee.objects.get(empid=username)
            name = employee.name
            id = employee.empid
            bid = employee.bid.bid
            data = {'name':name, 'id': id, 'bid':bid}
            banker = {}
            branch = {}
        return render(request, 'rootApp/user-profile.html', {'data':data, 'banker':banker, 'branch':branch})
    except Employee.DoesNotExist:
        return render(request, 'rootApp/user-profile.html', {'name':'Not Available', 'ID': 'Not Available'})
    