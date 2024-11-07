from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from empApp.forms import LoginForm, CreateCustomerForm, CreateEmployeeForm,CreateAccountForm
from empApp.models import CustomUser, Customer, Employee, PersonalBanker
from django.db import transaction
from empApp.decorators import role_required

# Create your views here.
def emp_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            employee = authenticate(request, username=username, password=password)
            if employee is not None and employee.user_type=='employee':
                login(request,employee)
                return redirect('home')
            else:
                return render(request, 'empApp/emp-login.html', {'form':form,'msg':'Invalid Credentials for Employee'})
    else:
        form = LoginForm()
        return render(request, 'empApp/emp-login.html', {'form': form, 'msg': 'Please Login to Continue'})


def user_logout(request):
    logout(request)
    return redirect('home')

def mgr_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                manager = authenticate(request, username=username, password=password)
                if manager is not None and manager.user_type=='manager':
                    login(request,manager)
                    return redirect('home')
                else:
                    return render(request,'empApp/mgr-login.html', {'form': form, 'msg': 'Invalid Manager Credentials'})
            except CustomUser.DoesNotExist:
                return render(request,'empApp/mgr-login.html', {'form': form, 'msg': f'User Does not Exists!!'})
    else:
        form = LoginForm()
        return render(request, 'empApp/mgr-login.html', {'form': form, 'msg': 'Please Login to Continue'})

def customer_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                customer = authenticate(request, username=username, password=password)
                print(customer)
                if customer is not None and customer.user_type=='customer':
                    login(request,customer)
                    return redirect('home')
                else:
                    return render(request,'empApp/cust-login.html', {'form': form, 'msg': 'Invalid Customer Credentials'})
            except CustomUser.DoesNotExist:
                return render(request,'empApp/cust-login.html', {'form': form, 'msg': f'User Does not Exists!!'})
    else:
        form = LoginForm()
        return render(request, 'empApp/cust-login.html', {'form': form, 'msg': 'Please Login to Continue'})

@role_required('manager', 'assistanMgr', 'employee', login_url='/')
def create_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            
            cssn = form.cleaned_data['cssn']
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            streetno = form.cleaned_data['streetno']
            aptno = form.cleaned_data['aptno']
  
            try:
                with transaction.atomic():
                    newCustomer = Customer.objects.create(
                        cssn = cssn,
                        name = name,
                        city = city,
                        state = state,
                        zipcode = zipcode,
                        streetno = streetno,
                        aptno = aptno
                    )
                    newCustomer.save()

                    loggedInEmployee = Employee.objects.get(empid=request.user.username)
                    print(loggedInEmployee.ssn)
                    newPersonalBanker = PersonalBanker.objects.create(
                        customerid = newCustomer,
                        bid = loggedInEmployee.bid,
                        essn = loggedInEmployee
                    )
                    newPersonalBanker.save()

                    username = newCustomer.customerid
                    password = f"{'_'.join(newCustomer.name.split(' '))}@{cssn}"
                    user = CustomUser.objects.create_user(username=username, user_type='customer')
                    user.set_password(password)
                    user.save()
                    return render(request, 'empApp/create-customer.html', {'form':form,"msg": "Customer created Successfully", 'id': newCustomer.customerid})
            except Customer.DoesNotExist:
                return render(request, 'empApp/create-customer.html', {'form':form,"msg": "Customer Does Not exist"})
            except IntegrityError as e:
                if 'Duplicate entry' in str(e):
                    return render(request, 'empApp/create-customer.html', {'form':form,"msg": "Customer already exists!"})
                return render(request, 'empApp/create-customer.html', {'form':form,"msg": f"{e}"})
            except Exception as e:
                return render(request, 'empApp/create-customer.html', {'form':form,"msg": f"{e}"})
    else:
        form = CreateCustomerForm()
        return render(request,"empApp/create-customer.html",{'form': form})
    return render(request, 'empApp/create-customer.html', {'form': CreateCustomerForm(), "msg": "Invalid request"})

@role_required('manager', 'assistanMgr', 'employee', login_url='/')
def open_account(request):
    try:
        customers = Customer.objects.all()
    except Exception as e:
        return render(request, 'empApp/open-acc.html', {'msg':f'Error!! {e}'})
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        customer_id = request.POST.get('customer')
        action = request.POST.get('action')
        selectID = request.POST.get('select')
        if search_query:
            try:
                customer = Customer.objects.get(customerid=search_query)
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':'Customer Not Found'})
        if customer_id:
            try:
                customer = Customer.objects.get(customerid=customer_id)
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':'Customer Not Found'})
        if selectID:
            customer = Customer.objects.get(customerid=selectID)
            # create account open form and display here
            openAccountForm = CreateAccountForm(request.POST)
            return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':f"Selected Customer:{customer.customerid}", 'oaform':openAccountForm})
        elif action=="list_all":
            return render(request, 'empApp/open-acc.html', {'customers': customers, 'data':customers})
    return render(request, 'empApp/open-acc.html', {'customers': customers})


    
@role_required('manager', 'assistanMgr', login_url='/')
def create_employee(request):
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            ssn = form.cleaned_data['ssn']
            name = form.cleaned_data['name']
            startdate = form.cleaned_data['startdate']
            teleno = form.cleaned_data['teleno']
            dependentname = form.cleaned_data['dependentname']
            bid = Employee.objects.get(empid=request.user.username).bid

            try:
                with transaction.atomic():

                    newEmployee = Employee.objects.create(
                        ssn = ssn,
                        name = name,
                        startdate = startdate,
                        teleno = teleno,
                        dependentname = dependentname,
                        bid = bid,
                    )
                    newEmployee.save()

                    username = newEmployee.empid
                    password = f"{'_'.join(newEmployee.name.split(' '))}@{newEmployee.ssn}"

                    user = CustomUser.objects.create_user(username=username,user_type='employee')
                    user.set_password(password)
                    user.save()
                    return render(request, 'empApp/create-emp.html', {'form':form,"msg": "Employee created Successfully", 'id':newEmployee.empid})
            except Customer.DoesNotExist:
                return render(request, 'empApp/create-emp.html', {'form':form,"msg": "Employee Does Not exist"})
            except IntegrityError as e:
                if 'Duplicate entry' in str(e):
                    return render(request, 'empApp/create-emp.html', {'form':form,"msg": "Employee already exists!"})
                return render(request, 'empApp/create-emp.html', {'form':form,"msg": f"{e}"})  
            except Exception as e:
                return render(request, 'empApp/create-emp.html', {'form':form,"msg": f"{e}"})
    else:
        form = CreateEmployeeForm()
        return render(request,"empApp/create-emp.html",{'form': form})
    return render(request, 'empApp/create-emp.html', {'form': CreateEmployeeForm(), "msg": "Invalid request"})


@role_required('manager', 'assistanMgr', 'employee', login_url='/')
def delete_customer(request):
    try:
        customers = Customer.objects.all()
    except Exception as e:
        return render(request, 'empApp/del-customer.html', {'msg':f'Error!! {e}'})
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        customer_id = request.POST.get('customer')
        action = request.POST.get('action')
        deleteid = request.POST.get('delete')
        if search_query:
            try:
                customer = Customer.objects.get(customerid=search_query)
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif customer_id:
            try:
                customer = Customer.objects.get(customerid=customer_id)
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif action=="list_all":
            return render(request, 'empApp/del-customer.html', {'customers': customers, 'data':customers})
        elif deleteid:
            with transaction.atomic():
                customer = Customer.objects.get(customerid=deleteid)
                user = CustomUser.objects.get(username=deleteid)
                customer.delete()
                user.delete()
            return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg': f"Customer {deleteid} deleted"})
    
    return render(request, 'empApp/del-customer.html', {'customers': customers})


@role_required('manager', 'assistanMgr', login_url='/')
def delete_employee(request):
    try:
        employees = Employee.objects.filter(bid = Employee.objects.get(empid=request.user.username).bid)
    except Exception as e:
        return render(request, 'empApp/del-employee.html', {'msg':f'Error!! {e}'})

    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        employee_id = request.POST.get('employee')
        action = request.POST.get('action')
        deleteid = request.POST.get('delete')
        
        print(employee_id)
        if search_query:
            try:
                employee = Employee.objects.get(empid=search_query)
                return render(request, 'empApp/del-employee.html', {'employees': employees, 'data':employee})
            except Employee.DoesNotExist as e:
                return render(request, 'empApp/del-employee.html', {'employees': employees, 'msg':'employee Not Found'})
        elif employee_id:
            try:
                employee = Employee.objects.get(empid=employee_id)
                return render(request, 'empApp/del-employee.html', {'employees': employees, 'data':employee})
            except Employee.DoesNotExist as e:
                return render(request, 'empApp/del-employee.html', {'employees': employees, 'msg':'employee Not Found'})
        elif action=="list_all":
            return render(request, 'empApp/del-employee.html', {'employees': employees, 'data':employees})
        elif deleteid:
            with transaction.atomic():
                employee = Employee.objects.get(empid=deleteid)
                user = CustomUser.objects.get(username=deleteid)
                employee.delete()
                user.delete()
            return render(request, 'empApp/del-employee.html', {'employees': employees, 'msg': f"employee {deleteid} deleted"})
    
    return render(request, 'empApp/del-employee.html', {'employees': employees})