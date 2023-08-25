from base64 import urlsafe_b64decode, urlsafe_b64encode
import base64
from pyexpat.errors import messages
from django.shortcuts import redirect, render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from authapp.models import CustomUser

from authapp.tokens import AccountActivationTokenGenerator
from .forms import CustomUserCreationForm,ForgotPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from authapp.tokens import account_activation_token
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_protect
from mainapp.utils import _retry_count

@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            user.reset_try=0
            user.save()
            return redirect('index')
        else:
            messages.info(
                request, 'Try again! username or password is incorrect')
          

    context = {}
    return render(request, 'auth/login.html', context)
def register(request):
    wasValidated=0
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            user = f.save()
            try:
                current_site = get_current_site(request)
                print(current_site.domain)
                subject = 'Please Activate Your Account'
                # load a template like get_template()
                # and calls its render() method immediately.
                user_id_str=str(user.id)
                userid_string_bytes = user_id_str.encode("ascii")
                
                userid_base64_bytes = base64.b64encode(userid_string_bytes)
                userid_base64_string = userid_base64_bytes.decode("ascii")

                message = render_to_string('auth/activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': userid_base64_string,
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })  
                # print(message)
                user.email_user(subject, message)
                return redirect('activation_sent')
            except Exception as e:
                print(e)
        else:
            print('error register')
            # f.attrs['class'] += ' my-css-class'
            # print(f)
        wasValidated=1        
    else:
        f = CustomUserCreationForm()
    context = {'wasValidated': wasValidated}

    return render(request, 'auth/register.html', {'form': f,'wasValidated': wasValidated})
def logout(request):
    auth_logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect("login")
    # resp = auth_logout()
    # resp['Refresh'] = '3;URL=/login/' # redirects after 3 seconds to /account/login
    # return resp
def activation_sent_view(request):
    return render(request, 'auth/activation_sent.html')
def activate(request, uidb64, token):
    try:
        userid_base64_bytes = uidb64.encode("ascii")
        userid_string_bytes = base64.b64decode(userid_base64_bytes)
        userid_string = userid_string_bytes.decode("ascii")
        user = CustomUser.objects.get(id=userid_string)
    # except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
    #     user = None
    except Exception as e:
        print(e)
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.signup_confirmation = True
        user.save()
        auth_login(request, user)
        return redirect('index')
    else:
        return render(request, 'auth/activation_invalid.html')

def forgot_password(request):
    if request.method == 'POST':
        f = ForgotPasswordForm(request.POST)
        print(f)
        if f.is_valid():
            try:
                current_site = get_current_site(request)
                print(current_site.domain)
                subject = 'Account Reset'
                emailUser = request.POST.get('email')
                users=CustomUser.objects.filter(email=emailUser , reset_try__lte=_retry_count)
                user=users[0]
                user_id_str=str(user.id)
                userid_string_bytes = user_id_str.encode("ascii")
                userid_base64_bytes = base64.b64encode(userid_string_bytes)
                userid_base64_string = userid_base64_bytes.decode("ascii")

                message = render_to_string('auth/password_reset_email_body.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': userid_base64_string,
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                user.reset_try+=1
                user.save()
                return redirect('password_reset_sent')
            except Exception as e:
                print(e)
        else:
            print('error passord reset')
            # f.attrs['class'] += ' my-css-class'
            # print(f)
        wasValidated=1        
    else:
        f = ForgotPasswordForm()
    return render(request, 'auth/forgot_password.html', {'form': f})
def password_reset(request, uidb64, token):
    try:
        userid_base64_bytes = uidb64.encode("ascii")
        userid_string_bytes = base64.b64decode(userid_base64_bytes)
        userid_string = userid_string_bytes.decode("ascii")
        user = CustomUser.objects.get(id=userid_string)
    except Exception as e:
        print(e)
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.reset_try=0
        user.save()
        auth_login(request, user)
        return redirect('index')
    else:
        return render(request, 'auth/activation_invalid.html')
def password_reset_sent_view(request):
    return render(request, 'auth/activation_sent.html')
def password_reset_activate(request, uidb64, token):
    try:
        userid_base64_bytes = uidb64.encode("ascii")
        userid_string_bytes = base64.b64decode(userid_base64_bytes)
        userid_string = userid_string_bytes.decode("ascii")
        user = CustomUser.objects.get(id=userid_string)
    # except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
    #     user = None
    except Exception as e:
        print(e)
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.signup_confirmation = True
        user.reset_try=0
        user.save()
        auth_login(request, user)
        return redirect('index')
    else:
        return render(request, 'auth/activation_invalid.html')

# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)
