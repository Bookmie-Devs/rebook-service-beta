from django import forms
from accounts.models import CustomUser

class PaymentForm(forms.Form):
    amount = forms.DecimalField(decimal_places=1, max_digits=7)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='username',)
    password = forms.PasswordInput()

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','middle_name','last_name','student_id','campus')
