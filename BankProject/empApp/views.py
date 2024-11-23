from django.db import IntegrityError, connection
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from empApp.forms import LoginForm, CreateCustomerForm, CreateEmployeeForm,CreateAccountForm, TransactionForm, SendMoneyForm, OpenLoanForm, PayLoanForm, LoanStatusForm
from empApp.models import CustomUser, Customer, Employee, PersonalBanker, AccOwner, Account, Transaction, Loans
from empApp.utils import list_all_users, list_user, add_accowner, list_all_accounts, list_account, add_loan, cust_list_all_acc
from django.db import transaction
from empApp.decorators import role_required
import datetime

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
                    try:
                        accOwner = AccOwner.objects.get(customerid=username)
                        if accOwner is not None:
                            with transaction.atomic():
                                #print(accOwner.accno.recentaccess)
                                lastLogin = CustomUser.objects.get(username=username).last_login
                                #print(lastLogin)
                                accOwner.accno.recentaccess = lastLogin
                                #print(accOwner.accno.recentaccess)
                                accOwner.accno.save()
                    except AccOwner.DoesNotExist:
                        pass
                    finally:
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
                        empid = loggedInEmployee
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
        if 'search_query' in request.POST:
            try:
                search_query = request.POST.get('search_query')
                customer = Customer.objects.get(customerid=search_query)
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif 'customer' in request.POST:
            try:
                customer_id = request.POST.get('customer')
                customer = Customer.objects.get(customerid=customer_id)
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':'Customer Not Found'})
            
        elif 'select' in request.POST:
            try:
                selectID = request.POST.get('select')
                customer = Customer.objects.get(customerid=selectID)

                initial_data = {
                    'accno':'',
                    'balance': '100',
                    'type' :'',
                    'interestsrate': '',
                    'overdraft' :'',
                    'customerid': customer
                }
                openAccountForm = CreateAccountForm(initial=initial_data)
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':f"Selected Customer:{customer.customerid}", 'oaform':openAccountForm})
            except Exception as e:
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':f"Error! {e}"})
                
        elif 'oaform' in request.POST:
            openAccountForm = CreateAccountForm(request.POST)
            #print(request.POST)
            if openAccountForm.is_valid():
                try:
                    with transaction.atomic():
                        accData = openAccountForm.save(commit=False)
                        accData.recentaccess = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        accData.save()
                        customer = Customer.objects.get(customerid=request.POST.get('customerid'))
                        """
                        accOwner = AccOwner.objects.create(accno=accData,customerid=customer)
                        print(accOwner.accno, accOwner.customerid)
                        accOwner.save()
                        """
                        data = add_accowner(request.POST.get('customerid'),accData.accno)
                        if data:
                            return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':f"Account Created"})
                        return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':f"Account Creation Failed", 'oaform':openAccountForm})      
                except Exception as e:
                    openAccountForm = CreateAccountForm()
                    return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':f"Failed to create Account {e}", 'oaform':openAccountForm})
            else:
                openAccountForm = CreateAccountForm()
                return render(request, 'empApp/open-acc.html', {'customers': customers, 'msg':f"Form Invalid", 'oaform':openAccountForm})
        elif 'action' in request.POST and request.POST.get('action') == 'list_all':
            return render(request, 'empApp/open-acc.html', {'customers': customers, 'data':customers})
    return render(request, 'empApp/open-acc.html', {'customers': customers})



@role_required('manager', 'assistanMgr', 'employee', login_url='/')
def delete_account(request):
    try:
        accounts = Account.objects.all()
    except Exception as e:
        return render(request, 'empApp/del-account.html', {'msg':f'Error!! {e}'})
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        account_id = request.POST.get('account')
        action = request.POST.get('action')
        deleteid = request.POST.get('delete')
        if search_query:
            try:
                account = Account.objects.get(accno=search_query)
                data = list_account(search_query)
                if data:
                    return render(request, 'empApp/del-account.html', {'accounts': accounts, 'data':data})
                return render(request, 'empApp/del-account.html', {'accounts': accounts, 'msg':'Unable to Fetch Account'})
            except Account.DoesNotExist as e:
                return render(request, 'empApp/del-account.html', {'accounts': accounts, 'msg':'Account Not Found'})
        elif account_id:
            try:
                account = Account.objects.get(accno=account_id)
                data = list_account(account_id)
                if data:
                    return render(request, 'empApp/del-account.html', {'accounts': accounts, 'data':data})
                return render(request, 'empApp/del-account.html', {'accounts': accounts, 'msg': 'Unable to Fecth Account'}) 
            except Account.DoesNotExist as e:
                return render(request, 'empApp/del-account.html', {'accounts': accounts, 'msg':'account Not Found'})
        elif action=="list_all":
            data = list_all_accounts()
            if data:
                return render(request, 'empApp/del-account.html', {'accounts': accounts, 'data':data})
            return render(request, 'empApp/del-account.html', {'accounts': accounts, 'msg': 'Unable to fetch all Accounts'})
        elif deleteid:
            print(deleteid)
            with transaction.atomic():
                account = Account.objects.get(accno=deleteid)
                account.delete()
            return render(request, 'empApp/del-account.html', {'accounts': accounts, 'msg': f"account {deleteid} deleted"})
    return render(request, 'empApp/del-account.html', {'accounts': accounts})



    
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
                data = list_user(search_query)
                if data:
                    return render(request, 'empApp/del-customer.html', {'customers': customers, 'data':data})
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg': 'Unable to Fecth User'})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif customer_id:
            try:
                customer = Customer.objects.get(customerid=customer_id)
                data = list_user(customer_id)
                if data:
                    return render(request, 'empApp/del-customer.html', {'customers': customers, 'data':data})
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg': 'Unable to Fecth User'}) 
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif action=="list_all":
            data = list_all_users()
            if data:
                return render(request, 'empApp/del-customer.html', {'customers': customers, 'data':data})
            return render(request, 'empApp/del-customer.html', {'customers': customers, 'msg':'Unable the Fetch all users'})            
        elif deleteid:
            print(deleteid)
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




def send_money(request):
    try:
        customer = Customer.objects.get(customerid=request.user.username)
        accounts = AccOwner.objects.filter(customerid=request.user.username)
        accno_choices = [(account.accno.accno, f"{account.accno.accno}  (${account.accno.balance})") for account in accounts if account.accno.type=="Checking"]
        if not accounts.exists() or not accno_choices:
            return render(request, 'empApp/send-money.html', {'msg': 'No Checking Bank Accounts Found'})
    except Customer.DoesNotExist:
        return render(request, 'empApp/send-money.html', {'msg': 'Unable to fetch Customer'})

    if request.method == 'POST':
        form = SendMoneyForm(
            request.POST, 
            accno_choices=accno_choices,
            )        
        if form.is_valid():
            accountNo = form.cleaned_data['accno']
            sendAmount = form.cleaned_data['amount']
            recvAccount = form.cleaned_data['recvacc']
            try:
                recvAcc = Account.objects.get(accno=recvAccount)
                recvCustomer = AccOwner.objects.get(accno=recvAcc)
            except Account.DoesNotExist:
                form = SendMoneyForm(accno_choices=accno_choices)
                return render(request, 'empApp/send-money.html', {'form': form, 'msg':'Recipient     Account Not Found'})
            except AccOwner.DoesNotExist:
                form = SendMoneyForm(accno_choices=accno_choices)
                return render(request, 'empApp/send-money.html', {'form': form, 'msg':'No owner found, Account may be inactive'})
            if recvAcc.type == "Checking":
                try:
                    account = Account.objects.get(accno=accountNo)
                    if account.balance-sendAmount > 0:
                        with transaction.atomic():
                            WDTransaction = Transaction.objects.create(
                                customerid = customer.customerid,
                                accno = accountNo,
                                date = timezone.now().date(),
                                time = timezone.now().time(),
                                code = 'WD',
                                amount = sendAmount
                            )
                            

                            CDTransaction = Transaction.objects.create(
                                customerid = recvCustomer.customerid.customerid,
                                accno = recvAcc.accno,
                                date = timezone.now().date(),
                                time = timezone.now().time(),
                                code = 'CD',
                                amount = sendAmount
                            )
                            
                            account.balance -= sendAmount

                            recvAcc.balance += sendAmount
                            account.save()
                            recvAcc.save()
                            WDTransaction.save()
                            CDTransaction.save()

                            form = SendMoneyForm(accno_choices=accno_choices)
                            return render(request, 'empApp/send-money.html', {'form': form, 'msg':f"Transaction Succesful: available balance {account.balance}"})
                    form = SendMoneyForm(accno_choices=accno_choices)
                    return render(request, 'empApp/send-money.html', {'form': form, 'msg':'Transaction Unsuccesful: Low Balance'})
                except Account.DoesNotExist:
                    form = SendMoneyForm(accno_choices=accno_choices)
                    return render(request, 'empApp/send-money.html', {'form': form, 'msg':'Unable to Process Account'})
            return render(request, 'empApp/send-money.html', {'form': form, 'msg':'Receiver not a valid checking Account'})
        print(form.errors)
        return render(request, 'empApp/send-money.html', {'form': form, 'msg':'Transaction Unsuccesful'})
        
    else:
        form = SendMoneyForm(accno_choices=accno_choices)
    return render(request, 'empApp/send-money.html', {'form': form})





def withdraw(request):
    try:
        customer = Customer.objects.get(customerid=request.user.username)
        accounts = AccOwner.objects.filter(customerid=request.user.username)
        accno_choices = [(account.accno.accno, f"{account.accno.accno}  (${account.accno.balance})") for account in accounts if account.accno.type=="Checking"]
        if not accounts.exists() or not accno_choices:
            return render(request, 'empApp/withdraw.html', {'msg': 'No Checking Bank Accounts Found'})
    except Customer.DoesNotExist:
        return render(request, 'empApp/withdraw.html', {'msg': 'Unable to fetch Customer'})

    if request.method == 'POST':
        form = TransactionForm(
            request.POST, 
            accno_choices=accno_choices,
            )        
        if form.is_valid():
            accountNo = form.cleaned_data['accno']
            withdrawAmount = form.cleaned_data['amount']
            try:
                account = Account.objects.get(accno=accountNo)
                if account.balance-withdrawAmount > 0:
                    with transaction.atomic():
                        custTransaction = Transaction.objects.create(
                            customerid = customer.customerid,
                            accno = accountNo,
                            date = timezone.now().date(),
                            time = timezone.now().time(),
                            code = 'WD',
                            amount = withdrawAmount
                        )
                        
                        account.balance -= withdrawAmount
                        account.save()
                        form = TransactionForm(accno_choices=accno_choices)
                        return render(request, 'empApp/withdraw.html', {'form': form, 'msg':f"Transaction Succesful: available balance {account.balance}"})
                form = TransactionForm(accno_choices=accno_choices)
                return render(request, 'empApp/withdraw.html', {'form': form, 'msg':'Transaction Unsuccesful: Low Balance'})
            except Account.DoesNotExist:
                form = TransactionForm(accno_choices=accno_choices)
                return render(request, 'empApp/withdraw.html', {'form': form, 'msg':'Unable to Process Account'})
        print(form.errors)
        return render(request, 'empApp/withdraw.html', {'form': form, 'msg':'Transaction Unsuccesful'})
        
    else:
        form = TransactionForm(accno_choices=accno_choices)
    return render(request, 'empApp/withdraw.html', {'form': form})


def deposit(request):
    try:
        customer = Customer.objects.get(customerid=request.user.username)
        accounts = AccOwner.objects.filter(customerid=request.user.username)
        accno_choices = [(account.accno.accno, f"{account.accno.accno} - {account.accno.type}  (${account.accno.balance})") for account in accounts if account.accno.type=="Checking" or account.accno.type == "Savings" or account.accno.type == "Money Market"]
        if not accounts.exists() or not accno_choices:
            return render(request, 'empApp/deposit.html', {'msg': 'No Bank Accounts Found'})
    except Customer.DoesNotExist:
        return render(request, 'empApp/deposit.html', {'msg': 'Unable to fetch Customer'})

    if request.method == 'POST':
        form = TransactionForm(
            request.POST, 
            accno_choices=accno_choices,
            )        
        if form.is_valid():
            accountNo = form.cleaned_data['accno']
            depositAmount = form.cleaned_data['amount']
            try:
                account = Account.objects.get(accno=accountNo)
                with transaction.atomic():
                    custTransaction = Transaction.objects.create(
                        customerid = customer.customerid,
                        accno = accountNo,
                        date = timezone.now().date(),
                        time = timezone.now().time(),
                        code = 'CD',
                        amount = depositAmount
                    )
                    account.balance += depositAmount
                    account.save()
                    form = TransactionForm(accno_choices=accno_choices)
                    return render(request, 'empApp/deposit.html', {'form': form, 'msg':f"Transaction Succesful: available balance {account.balance}"})
            except Account.DoesNotExist:
                form = TransactionForm(accno_choices=accno_choices)
                return render(request, 'empApp/deposit.html', {'form': form, 'msg':'Unable to Process Account'})
        print(form.errors)
        return render(request, 'empApp/deposit.html', {'form': form, 'msg':'Transaction Unsuccesful'})
        
    else:
        form = TransactionForm(accno_choices=accno_choices)
    return render(request, 'empApp/deposit.html', {'form': form})









@role_required('manager', 'assistanMgr', 'employee', login_url='/')
def open_loan(request):
    try:
        customers = Customer.objects.all()
        currentEmp = Employee.objects.get(empid = request.user.username)
        #print(currentEmp.bid)
    except Exception as e:
        return render(request, 'empApp/open-loan.html', {'msg':f'Error!! {e}'})
    
    if request.method == 'POST':
        if 'search_query' in request.POST:
            try:
                search_query = request.POST.get('search_query')
                customer = Customer.objects.get(customerid=search_query)
                return render(request, 'empApp/open-loan.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif 'customer' in request.POST:
            try:
                customer_id = request.POST.get('customer')
                customer = Customer.objects.get(customerid=customer_id)
                return render(request, 'empApp/open-loan.html', {'customers': customers, 'data':customer})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':'Customer Not Found'})
            
        elif 'select' in request.POST:
            try:
                selectID = request.POST.get('select')
                customer = Customer.objects.get(customerid=selectID)

                #print(currentEmp.bid)
                initial_data = {
                    'customerid': customer.customerid,
                    'bid': currentEmp.bid,
                }
                openLoanForm = OpenLoanForm(initial=initial_data)
                return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':f"Selected Customer:{customer.customerid}", 'oaform':openLoanForm})
            except Exception as e:
                return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':f"Error! {e}"})
                
        elif 'oaform' in request.POST:
            openLoanForm = OpenLoanForm(request.POST)
            #print(request.POST)
            if openLoanForm.is_valid():
                try:
                    with transaction.atomic():
                        customer = openLoanForm.cleaned_data['customerid']
                        #print(type(customer.customerid))
                        bid = openLoanForm.cleaned_data['bid']
                        amount = openLoanForm.cleaned_data['amount']
                        interestRate = openLoanForm.cleaned_data['interestrate']
                        monthlyrepayment = openLoanForm.cleaned_data['monthlyrepayment']

                        loanAmount = amount+(amount*(interestRate/100))

                        loanAccount = Account.objects.create(
                            balance= amount,
                            type="Loan",
                            interestsrate= interestRate,
                            recentaccess = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        )

                        data = add_loan(customer.customerid,loanAccount.accno,bid.bid,loanAmount,monthlyrepayment,loanAmount)
                        if data:
                            return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':f"Loan Account Created"})
                        return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':f"Account Creation Failed", 'oaform':openLoanForm})      
                except Exception as e:
                    openLoanForm = OpenLoanForm()
                    return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':f"Failed to create Account {e}", 'oaform':openLoanForm})
            else:
                print(openLoanForm.errors)
                openLoanForm = OpenLoanForm()
                return render(request, 'empApp/open-loan.html', {'customers': customers, 'msg':f"Form Invalid", 'oaform':openLoanForm})
        elif 'action' in request.POST and request.POST.get('action') == 'list_all':
            return render(request, 'empApp/open-loan.html', {'customers': customers, 'data':customers})
    return render(request, 'empApp/open-loan.html', {'customers': customers})




def pay_loan(request):
    try:
        customer = Customer.objects.get(customerid=request.user.username)
        accounts = AccOwner.objects.filter(customerid=request.user.username)
        accno_choices = [(account.accno.accno, f"{account.accno.accno}  (${account.accno.balance})") for account in accounts if account.accno.type=="Checking"]
        loans = Loans.objects.filter(customerid=request.user.username)
        loan_acc_choices = [(account.accno.accno, f"{account.accno.accno}  (${account.amount})") for account in loans if account.accno.type=="Loan"]
        if not accounts.exists() or not accno_choices:
            return render(request, 'empApp/pay-loan.html', {'msg': 'No Checking Bank Accounts Found'})
    except Customer.DoesNotExist:
        return render(request, 'empApp/pay-loan.html', {'msg': 'Unable to fetch Customer'})

    if request.method == 'POST':
        form = PayLoanForm(
            request.POST, 
            accno_choices=accno_choices,
            loanAccno_choices = loan_acc_choices,
            )        
        if form.is_valid():
            accountNo = form.cleaned_data['accno']
            sendAmount = form.cleaned_data['amount']
            loanAccountNo = form.cleaned_data['loanAccno']

            
            try:
                account = Account.objects.get(accno=accountNo)
                loanAccount = Loans.objects.get(accno=loanAccountNo)
                if account.balance-sendAmount > 0:
                    with transaction.atomic():
                        custTransaction = Transaction.objects.create(
                            customerid = customer.customerid,
                            accno = accountNo,
                            date = timezone.now().date(),
                            time = timezone.now().time(),
                            code = 'WD',
                            amount = sendAmount
                        )
                        
                        loanTransaction = Transaction.objects.create(
                            customerid = customer.customerid,
                            accno = loanAccountNo,
                            date = timezone.now().date(),
                            time = timezone.now().time(),
                            code = 'CD',
                            amount = sendAmount
                        )
                        
                        account.balance -= sendAmount
                        account.save()

                        loanAccount.outstandingamount -= sendAmount
                        loanAccount.save()
                        

                        form = PayLoanForm(accno_choices=accno_choices, loanAccno_choices = loan_acc_choices)
                        return render(request, 'empApp/pay-loan.html', {'form': form, 'msg':f"Transaction Succesful: available balance {account.balance}"})
                form = PayLoanForm(accno_choices=accno_choices, loanAccno_choices = loan_acc_choices)
                return render(request, 'empApp/pay-loan.html', {'form': form, 'msg':'Transaction Unsuccesful: Low Balance'})
            except Account.DoesNotExist:
                form = PayLoanForm(accno_choices=accno_choices, loanAccno_choices = loan_acc_choices)
                return render(request, 'empApp/pay-loan.html', {'form': form, 'msg':'Unable to Process Account'})
        print(form.errors)
        return render(request, 'empApp/pay-loan.html', {'form': form, 'msg':'Transaction Unsuccesful'})
        
    else:
        form = PayLoanForm(accno_choices=accno_choices, loanAccno_choices = loan_acc_choices)
    return render(request, 'empApp/pay-loan.html', {'form': form})


def loan_status(request):
    try:
        loans = Loans.objects.filter(customerid=request.user.username)
    except Exception as e:
        return render(request, 'empApp/loan-status.html', {'msg':f'Error!! {e}'})
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        loanNum = request.POST.get('loan')
        action = request.POST.get('action')
        deleteid = request.POST.get('delete')
        if search_query:
            try:
                loan = Loans.objects.get(loanno=search_query)
                #data = list_user(search_query)
                #if data:
                return render(request, 'empApp/loan-status.html', {'loans': loans, 'data': loan})
                return render(request, 'empApp/loan-status.html', {'loans': loans, 'msg': 'Unable to Fecth Loan'})
            except Loans.DoesNotExist as e:
                return render(request, 'empApp/loan-status.html', {'loans': loans, 'msg':'Loan Not Found'})
        elif loanNum:
            try:
                loan= Loans.objects.get(loanno=loanNum)
                return render(request, 'empApp/loan-status.html', {'loans': loans, 'data':loan})
                return render(request, 'empApp/loan-status.html', {'loans': loans, 'msg': 'Unable to Fecth User'}) 
            except Loans.DoesNotExist as e:
                return render(request, 'empApp/loan-status.html', {'loans': loans, 'msg':'Loan Not Found'})
        elif action=="list_all":
            return render(request, 'empApp/loan-status.html', {'loans': loans, 'data':loans})
            return render(request, 'empApp/loan-status.html', {'loans': loans, 'msg':'Unable the Fetch all users'})            
    return render(request, 'empApp/loan-status.html', {'loans': loans})


@role_required('manager', 'assistanMgr', 'employee', login_url='/')
def list_all_customer(request):
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
                data = list_user(search_query)
                if data:
                    return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'data':data})
                return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'msg': 'Unable to Fecth User'})
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif customer_id:
            try:
                customer = Customer.objects.get(customerid=customer_id)
                data = list_user(customer_id)
                if data:
                    return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'data':data})
                return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'msg': 'Unable to Fecth User'}) 
            except Customer.DoesNotExist as e:
                return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'msg':'Customer Not Found'})
        elif action=="list_all":
            data = list_all_users()
            if data:
                return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'data':data})
            return render(request, 'empApp/list-all-cust.html', {'customers': customers, 'msg':'Unable the Fetch all users'})            
    return render(request, 'empApp/list-all-cust.html', {'customers': customers})


#@role_required('customer', login_url='/')
def cust_list_all_account(request):
    try:
        accounts = cust_list_all_acc(request.user.username)
    except Exception as e:
        return render(request, 'empApp/cust-list-all-acc.html', {'msg':f'Error!! {e}'})
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        acc_number = request.POST.get('account')
        action = request.POST.get('action')
        if search_query:
            try:
                account = Account.objects.get(accno=search_query)
                return render(request, 'empApp/cust-list-all-acc.html', {'accounts': accounts, 'data':account})
            except Account.DoesNotExist as e:
                return render(request, 'empApp/cust-list-all-acc.html', {'accounts': accounts, 'msg':'Account Not Found'})
        elif acc_number:
            try:
                account = Account.objects.get(accno=acc_number)
                return render(request, 'empApp/cust-list-all-acc.html', {'accounts': accounts, 'data':account}) 
            except Account.DoesNotExist as e:
                return render(request, 'empApp/cust-list-all-acc.html', {'accounts': accounts, 'msg':'Account Not Found'})
        elif action=="list_all":
            return render(request, 'empApp/cust-list-all-acc.html', {'accounts': accounts, 'acc_data':accounts})            
    return render(request, 'empApp/cust-list-all-acc.html', {'accounts': accounts})
