from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from empApp.forms import LoginForm, CreateCustomerForm, CreateEmployeeForm
from empApp.models import CustomUser, Customer, Employee
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
                user = CustomUser.objects.get(username=username)
                print(user.password)
                print(password)
            
                manager = authenticate(request, username=username, password=password)
                
                #print(manager.user_type)
                if manager is not None and manager.user_type=='manager':
                    login(request,manager)
                    print("done")
                    return redirect('home')
                else:
                    return render(request,'empApp/mgr-login.html', {'form': form, 'msg': 'Invalid Manager Credentials'})
            except CustomUser.DoesNotExist:
                return render(request,'empApp/mgr-login.html', {'form': form, 'msg': f'User Does not Exists!!'})

    else:
        form = LoginForm()
        return render(request, 'empApp/mgr-login.html', {'form': form, 'msg': 'Please Login to Continue'})

@role_required('manager', 'assistanMgr', login_url='/mgr-login/')
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
  
            username= '_'.join(name.split(' '))
            password = f"{username}@{cssn}"
            #print(password)
            
            try:
                with transaction.atomic():

                    customer = Customer.objects.create(
                        cssn = cssn,
                        name = name,
                        city = city,
                        state = state,
                        zipcode = zipcode,
                        streetno = streetno,
                        aptno = aptno
                    )

                    customer.save()

                    user = CustomUser.objects.create_user(username=username,password=password, user_type='customer')
                    user.save()
                    return render(request, 'empApp/create-customer.html', {'form':form,"msg": "Customer created Successfully"})
            except Customer.DoesNotExist:
                return render(request, 'empApp/create-customer.html', {'form':form,"msg": "Customer Does Not exist"})
            except Exception as e:
                return render(request, 'empApp/create-customer.html', {'form':form,"msg": f"{e}"})
    else:
        form = CreateCustomerForm(request.POST)
        return render(request,"empApp/create-customer.html",{'form': form})
    


@role_required('manager', 'assistanMgr', login_url='/mgr-login/')
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

                    user = CustomUser.objects.create_user(username=username,password=password, user_type='employee')
                    user.save()
                    return render(request, 'empApp/create-emp.html', {'form':form,"msg": "Employee created Successfully"})
            except Customer.DoesNotExist:
                return render(request, 'empApp/create-emp.html', {'form':form,"msg": "Employee Does Not exist"})
            except Exception as e:
                return render(request, 'empApp/create-emp.html', {'form':form,"msg": f"{e}"})
    else:
        form = CreateEmployeeForm(request.POST)
        return render(request,"empApp/create-emp.html",{'form': form})

    
def delete_customer(request):
    try:
        customers = Customer.objects.all()
        choices = []
        for customer in customers:
            choices.append((f"{customers}"))
    except Exception as e:
        print(e)

    return render(request, 'empApp/del-customer.html', {'customers': customers})