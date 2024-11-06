from django.shortcuts import render
from empApp.decorators import role_required
from empApp.models import Employee, Customer, PersonalBanker
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
            bid = personalBanker.essn.bid.bid
            data = {'name':name, 'id': id}
            banker = {'name':personalBanker.essn.name, 'teleno': personalBanker.essn.teleno,'bid':bid}
        else:
            employee = Employee.objects.get(empid=username)
            name = employee.name
            id = employee.empid
            bid = employee.bid.bid
            data = {'name':name, 'id': id, 'bid':bid}
            banker = {}
        return render(request, 'rootApp/user-profile.html', {'data':data, 'banker':banker})
    except Employee.DoesNotExist:
        return render(request, 'rootApp/user-profile.html', {'name':'Not Available', 'ID': 'Not Available'})
    