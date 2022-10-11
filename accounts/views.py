from email import message
from lib2to3.pgen2.tokenize import generate_tokens
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth.models import auth
from .forms import UserLogin, UserRegister
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views.generic import View
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
from .utils import token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings










# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST or None)
        if form.is_valid():

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            
        
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
      
        # email = request.POST['email']
        # password = request.POST['password']
        # confirm_password = request.POST['confirm_password']

            if password==confirm_password:
        
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email is already taken')
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(email=email, password=password, 
                                            first_name=first_name, last_name=last_name)
                    user.is_active = False
                    user.save()



                    current_site = get_current_site(request)
                    email_subject = "Activate your account"
                    message=render_to_string('activate.html',
                    {
                        'user':user,
                        'domain':current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                        'token':token_generator.make_token(user) 
                    })

                    email_message = EmailMessage(
                        email_subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        )

                    email_message.send(fail_silently=False)
                    messages.success(request, "You have successfully registered")
                    
                    return redirect('accounts:login')


            else:
                messages.warning(request, 'Both passwords are not matching')
                return redirect('accounts:register')
            
        else:
            messages.info(request, 'Server error')
            return redirect('accounts:register')

    else:
        form = UserRegister()
        context = {
            'form':form
        }
        return render(request, 'signup.html', context)





def login(request):
    if request.method == 'POST':
        form = UserLogin(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
     
         
            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                if user.is_admin or user.is_superuser:
                    return redirect(reverse('admin:index'))
                else:

                    return redirect('core:home')
            else:
                messages.warning(request, 'Invalid Email or Password')
                return redirect('accounts:login')
        else:
            messages.warning(request, 'Server error')
            return redirect('accounts:login')


    else:
        form = UserLogin()
        context = {
                'form':form
            }
        return render(request, 'login.html', context)


@login_required(redirect_field_name='accounts:login')
def logout(request):
    auth.logout(request)
    return redirect('core:home')


class VerificationView(View):
   
    def get(self, request, uidb64, token):
       
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'You have successfully activated your account')
            return redirect('accounts:login')
            

        return render(request, 'activation_failed.html', status=401)









from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes




def password_reset_request(request):
    data = password_reset_form.cleaned_data['email']
    associated_users = User.objects.filter(Q(email=data))
    if associated_users.exists():
        for user in associated_users:
            subject = "Password Reset Requested"
            email_template_name = "password_reset_email.txt"
            c = {
					"email":user.email,
 					'domain':get_current_site(request).domain,
 					'site_name': 'Website',
 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
 					"user": user,
 					'token': default_token_generator.make_token(user),
 					'protocol': 'http',
 				}
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
            except BadHeaderError:  
                return HttpResponse('Invalid header found.')
            return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request, "password_reset.html", context={"password_reset_form":password_reset_form})


# def password_reset_request(request):
#     data = password_reset_form.cleaned_data['email']
#     associated_users = User.objects.filter(Q(email=data))
#     if associated_users.exists():
# 	    for user in associated_users:
# 		    subject = "Password Reset Requested"
# 		    email_template_name = "password_reset_email.txt"
# 		    c = {
# 					"email":user.email,
# 					'domain':get_current_site(request).domain,
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 		    email = render_to_string(email_template_name, c)
# 		    try:
# 				send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
# 		    except BadHeaderError:
# 			    return HttpResponse('Invalid header found.')
# 		    return redirect ("/password_reset/done/")
# 	password_reset_form = PasswordResetForm()
# 	return render(request, "password_reset.html", context={"password_reset_form":password_reset_form})



