from django import forms

class EmployeeLoginForm(forms.Form):
    essn = forms.IntegerField(label='Employee SSN', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['essn'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your SSN'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})