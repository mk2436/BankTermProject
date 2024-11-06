from django import forms

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