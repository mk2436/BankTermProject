from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from empApp.forms import LoginForm, CreateCustomerForm
from django.contrib.auth import authenticate, login, logout
from empApp.models import CustomUser, Customer
from django.db import transaction

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
            try:
                user = CustomUser.objects.get(username='John_Doe')
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
            """
            return render(request,"empApp/create-customer.html",{'form': form})"""
    else:
        form = CreateCustomerForm(request.POST)
        return render(request,"empApp/create-customer.html",{'form': form})
    
def delete_customer(request):
    try:
        customers = Customer.objects.all()
        choices = []
        for customer in customers:
            choices.append((f"{customers}"))
    except Exception as e:
        print(e)

    return render(request, 'empApp/del-customer.html', {'customers': customers})