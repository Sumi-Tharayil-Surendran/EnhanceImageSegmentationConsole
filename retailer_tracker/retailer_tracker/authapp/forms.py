
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from mainapp.utils import _retry_count



class CustomUserCreationForm(forms.Form):
    #username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Username'}), min_length=4, max_length=150)
    email = forms.EmailField(label=False,widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(label=False,widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label=False,widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))  
    
    # products   = forms.ModelMultipleChoiceField(queryset=Product.objects.all(),
    #                                            widget=forms.CheckboxSelectMultiple,required=True)
    #class UserProfile(AbstractUser):
    #Products = forms.ManyToManyField(Product)

    # def clean_username(self):
    #     username = self.cleaned_data['username'].lower()
    #     r = User.objects.filter(username=username)
    #     if r.count():
    #         raise  ValidationError("Username already exists")
    #     return username

    def clean_email(self):
        print('register:clean_email')
        UserModel = get_user_model()
        email = self.cleaned_data['email'].lower()
        r = UserModel.objects.filter(email=email)
        print('register:clean_email',str(r.count()))
        print('register:clean_email',email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        print('register:clean_password2')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        print('register:save')
        UserModel = get_user_model()
        user = UserModel.objects.create_user(
            #self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
    # class Meta:
    #   UserModel = get_user_model()
    #   model = UserModel #this is the "YourCustomUser" that you imported at the top of the file  
    #   fields = ('email', 'password1', 'password2')
class ForgotPasswordForm(forms.Form):
    #username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Username'}), min_length=4, max_length=150)
    email = forms.EmailField(label=False,widget=forms.TextInput(attrs={'placeholder': 'email'}))
    def clean_email(self):
        print('forgot password:clean_email')
        UserModel = get_user_model()
        email = self.cleaned_data['email'].lower()
        r = UserModel.objects.filter(email=email,reset_try__lte=_retry_count)
        print('forgot password:clean_email',str(r.count()))
        if r.count()==0:
            raise  ValidationError("Invalid Email")
        return email
    # class Meta: