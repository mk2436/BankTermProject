from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your Password'})