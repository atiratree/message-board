import random
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse

from board.forms import MessageForm, LoginForm, RegisterForm
from board.models import Message

def index(request):     
    form = None   
    if request.method == 'POST' and request.user.is_authenticated():
        reqForm = MessageForm(request.POST)
        if reqForm.is_valid():                       
            msg =  Message(date= timezone.now(), title=reqForm.cleaned_data["title"], content=reqForm.cleaned_data["content"], author=request.user)
            msg.save() 
            return redirect(reverse('board:index'))
        else:
            form = reqForm 
    
    if form is None:
       form = MessageForm()
    
    context = {'messages': Message.objects.order_by('-date'), 'form': form, 'auth': request.user.is_authenticated()}
    return render(request, 'board/index.html', context)
    
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        reqForm = LoginForm(request.POST)
        if reqForm.is_valid():
            user = auth.authenticate(username=reqForm.cleaned_data["username"], password=reqForm.cleaned_data["password"])
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('/')
        return render(request, 'board/login.html', {'form': form, 'errorMsg': 'Bad username or password!'})
    return render(request, 'board/login.html', {'form': form})
    
def logout(request):
    auth.logout(request)
    return redirect('/')
    
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        reqForm = RegisterForm(request.POST)
        if reqForm.is_valid() and reqForm.cleaned_data["password"] == reqForm.cleaned_data["password2"]:
            try:
                User.objects.create_user(reqForm.cleaned_data["username"], None, reqForm.cleaned_data["password"])
                return render(request, 'board/login.html', {'errorMsg': 'user created! pls login', 'form':LoginForm()})
            except:
                return render(request, 'board/register.html', {'form': form, 'errorMsg': 'Username taken!'})
        else:
            return render(request, 'board/register.html', {'form': form, 'errorMsg': 'Passwords didn\'t match'})
        return render(request, 'board/register.html', {'form': form, 'errorMsg': 'Pls fill all forms and repeat the password twice'})
    return render(request, 'board/register.html', {'form': form})
