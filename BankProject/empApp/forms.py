from django import forms
from .models import Account, AccOwner, Customer, Loans, Branch
from django.core.exceptions import ValidationError

from django import forms
from .models import Account, Customer

class CreateAccountForm(forms.ModelForm):
    # Use ModelChoiceField to associate with Customer (hidden input)
    customerid = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        label='Customer ID',
        widget=forms.HiddenInput,
        required=True  # Make customerid field required
    )
    
    # Override other fields to make them required
    balance = forms.DecimalField(
        label='Balance',
        required=True,  # Make balance field required
        min_value=0,    # Optionally set a minimum value, e.g., balance cannot be negative
    )

    type = forms.ChoiceField(
        choices=Account.ACCOUNT_TYPE_CHOICES,  # This will use the choices from the Account model
        required=True,  # Make type field required
        label='Account Type'
    )

    interestsrate = forms.DecimalField(
        label='Interest Rate',
        required=True,  # Make interest rate field required
        min_value=0,    # Optionally set a minimum value
    )

    overdraft = forms.DecimalField(
        label='Overdraft',
        required=True,  # Make overdraft field required
        min_value=0,    # Optionally set a minimum value
    )

    class Meta:
        model = Account
        fields = ['balance', 'type', 'interestsrate', 'overdraft', 'customerid']
        labels = {
            'customerid': 'Customer ID',
            'balance': 'Balance',
            'type': 'Account Type',
            'interestsrate': 'Interest Rate',
            'overdraft': 'Overdraft',
        }

    def save(self, commit=True):
        # First, save the Account instance
        account = super().save(commit=False)

        # Find the Customer instance by the customerid selected
        customer = self.cleaned_data['customerid']

        # Create and associate the AccOwner instance
        if commit:
            account.save()  # Save the Account instance first
            AccOwner.objects.create(customerid=customer, accno=account)  # Link the Account to the Customer

        return account



class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your Password'})

class CreateCustomerForm(forms.Form):
    cssn = forms.IntegerField(label='Customer SSN',required=True)
    name = forms.CharField(label='Customer Name', max_length=100, required=True)
    city = forms.CharField(label='City', max_length=100, required=True)
    state = forms.CharField(label='State', max_length=100, required=True)
    zipcode = forms.IntegerField(label='ZipCode',required=True)
    streetno = forms.IntegerField(label='Street No.',required=True)
    aptno = forms.CharField(label='Apt No.',required=True,max_length=100)

class CreateEmployeeForm(forms.Form):
    ssn = forms.IntegerField(label='Employee SSN',required=True)
    name = forms.CharField(label='Employee Name', max_length=100, required=True)
    startdate = forms.DateField(label='Start Date', required=True)
    teleno = forms.CharField(label='Tele No',required=True)
    dependentname = forms.CharField(label='Dependent Name', max_length=100)
    

class ListCustomers(forms.Form):
    cssn = forms.ChoiceField(label="Select an option",required=False)
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['cssn'].choices = choices


class SendMoneyForm(forms.Form):
    senderAccount = forms.ChoiceField(
        choices = None,
        label='Sender Account',
        required=True,
    )

    receiverAccount = forms.CharField(
        label='Receiver Account',
        required=True,
    )



class TransactionForm(forms.Form):
    CREDIT = 'CD'
    WITHDRAW = 'WD'
    TRANSACTION_CHOICES = [
        (CREDIT, 'Credit'),
        (WITHDRAW, 'Withdraw'),
    ]
    accno = forms.ChoiceField(label='Account Number')
    amount = forms.DecimalField(max_digits=15, decimal_places=2, required=True, label='Amount', widget=forms.NumberInput(attrs={'step': '0.01'}))
    
    def __init__(self, *args, **kwargs):
        accno_choices = kwargs.pop('accno_choices', [])
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['accno'].choices = accno_choices


class SendMoneyForm(forms.Form):
    CREDIT = 'CD'
    TRANSACTION_CHOICES = [
        (CREDIT, 'Credit'),
    ]

    accno = forms.ChoiceField(label='Account Number')
    amount = forms.DecimalField(max_digits=15, decimal_places=2, required=True, label='Amount', widget=forms.NumberInput(attrs={'step': '0.01'}))
    recvacc= forms.CharField(label='Reciever Account Number', required=True)

    def __init__(self, *args, **kwargs):
        accno_choices = kwargs.pop('accno_choices', [])
        super(SendMoneyForm, self).__init__(*args, **kwargs)
        self.fields['accno'].choices = accno_choices


class OpenLoanForm(forms.Form):
    customerid = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        label='Customer ID',
        widget=forms.HiddenInput,
        required=True  # Make customerid field required
    )
    

    bid = forms.ModelChoiceField(
        queryset= Branch.objects.all(),
        label='BID',
        widget=forms.HiddenInput,
        required=True  # Make customerid field required
    )

    amount = forms.DecimalField(
        label="Loan Amount",
        required=True
    )

    monthlyrepayment = forms.DecimalField(
        label="Monthly Repayment",
        required=True
    )

    interestrate = forms.DecimalField(
        label="Interest Rate",
        required=True
    )

     