from django import forms
from .models import Account, AccOwner, Customer
from django.core.exceptions import ValidationError

class CreateAccountForm(forms.ModelForm):
    # Use ModelChoiceField to associate with Customer
    customerid = forms.ModelChoiceField(queryset=Customer.objects.all(), label='Customer ID', widget=forms.HiddenInput)

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