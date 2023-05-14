from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from user.forms import UserLoginForm, UserRegisterForm
from user.models import User

def logout_view(request):
    logout(request)
    return redirect('/')

def log_reg_view(request):

    if request.method == 'GET':

        reg_form = UserRegisterForm
        log_form = UserLoginForm

        return render(request, 'log_reg.html', context={
            'user': None if request.user.is_anonymous else request.user,
            'reg_form': reg_form,
            'log_form': log_form,
        })

    if request.method == 'POST':
        log_form = UserLoginForm(data=request.POST)
        reg_form = UserRegisterForm(data=request.POST)
        
        
        if log_form.is_valid():

            user = authenticate(
                email=log_form.cleaned_data.get('email'),
                password=log_form.cleaned_data.get('password')
            )

            if user:
                login(request, user=user)
                return redirect('/')
            else:
                log_form.add_error(
                    'email', 'email or password is not correct')
                

        if reg_form.is_valid():
            
            if not User.objects.filter(email=reg_form.cleaned_data.get('email')).exists():

                if reg_form.cleaned_data.get('password') == reg_form.cleaned_data.get('confirmpassword'):
                    
                    user = User.objects.create_user(
                    email=reg_form.cleaned_data.get('email'),
                    name=reg_form.cleaned_data.get('name'),
                    password=reg_form.cleaned_data.get('confirmpassword'),
                    confirmpassword=reg_form.cleaned_data.get('confirmpassword')
                    )
                    return redirect('/login/')
                    
                else:
                    reg_form.add_error('confirmpassword',
                                    'passwords are different')
            
            else:
                reg_form.add_error('email',
                                   'email is not unique')

            

        return render(request, 'log_reg.html', context={
            'user': None if request.user.is_anonymous else request.user,
            'log_form': log_form,
            'reg_form': reg_form
        })
