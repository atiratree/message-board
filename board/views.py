import random
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse

from board.forms import MessageForm
from board.models import Message

def index(request):     
    form = None   
    if request.method == 'POST':
        reqForm = MessageForm(request.POST)
        if reqForm.is_valid():
            user = User(username='Generic' + str(random.randint(0,99999999)))
            user.set_password('new password')
            user.save()
                       
            msg =  Message(date= timezone.now(), title=reqForm.cleaned_data["title"], content=reqForm.cleaned_data["content"], author=user)
            msg.save() 
            return redirect(reverse('board:index'))
        else:
            form = reqForm 
    
    if form is None:
        form = MessageForm()
    
    context = {'messages': Message.objects.all(), 'form': form}
    return render(request, 'board/index.html', context)
