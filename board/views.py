from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import auth
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy

from board.forms import MessageForm, LoginForm, RegisterForm, SearchForm
from board.models import Message

SEARCH_SESSION = 'search'
SEARCH_PARAM = 'search'
ITEMS_PER_PAGE = 10

def index(request):
    form = None

    if request.method == 'POST':
        if request.GET.get(SEARCH_PARAM) == "false":
            reqForm = MessageForm(request.POST)
            if request.user.is_authenticated() and reqForm.is_valid():
                msg = Message(date=timezone.now(), title=reqForm.cleaned_data["title"], content=reqForm.cleaned_data["content"], author=request.user)
                msg.save()
                __clean_session(request)
                return redirect(reverse('board:index'))
            else:
                form = reqForm
        else:
            reqForm = SearchForm(request.POST)
            if reqForm.is_valid():
                request.session[SEARCH_SESSION] = reqForm.cleaned_data
                return redirect(reverse('board:index'))

    if form is None:
        form = MessageForm()

    filterContent, filterAuthor = __getFilters(request)
    searchForm = SearchForm(initial={'search': filterContent, 'searchAuthor': filterAuthor })

    dbMessages = Message.objects.filter((Q(title__icontains=filterContent) | Q(content__icontains=filterContent))
                                         & Q(author__username__icontains=filterAuthor)).order_by('-date')
    messages = __get_paginated_objects(dbMessages , request.GET.get('page'), ITEMS_PER_PAGE)

    context = {'messages': messages, 'form': form, 'auth': request.user.is_authenticated(), 'search_form':searchForm}
    return render(request, 'board/index.html', context)

def login(request):
    errorMessage = None
    username = ''

    if request.method == 'POST':
        reqForm = LoginForm(request.POST)
        if reqForm.is_valid():
            username = reqForm.cleaned_data["username"]
            password = reqForm.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                __clean_session(request)
                return redirect('/')
        errorMessage = 'Bad username or password!'

    context = {'form': LoginForm(initial={'username': username})}
    if errorMessage is not None:
        context['errorMsg'] = errorMessage
    return render(request, 'board/login.html', context)
    
def logout(request):
    auth.logout(request)
    return redirect('/')
    
def register(request):
    errorMessage = None
    username = ''

    if request.method == 'POST':
        reqForm = RegisterForm(request.POST)
        if reqForm.is_valid():
            password = reqForm.cleaned_data["password"]
            username = reqForm.cleaned_data["username"]
            if password == reqForm.cleaned_data["password2"]:
                if len(password) > 7:
                    try:
                        User.objects.create_user(username, None, password)
                        return render(request, 'board/login.html', {'errorMsg': 'user created! please login', 'form':LoginForm()})
                    except:
                        errorMessage = 'Username taken!'
                else:
                    errorMessage = 'Password must be at least 8 characters long!'
            else:
                errorMessage = 'Passwords didn\'t match'
        else:
            errorMessage = 'Please fill all forms and repeat the password twice'

    context = {'form': RegisterForm(initial={'username': username})}
    if errorMessage is not None:
        context['errorMsg'] = errorMessage
    return render(request, 'board/register.html', context)

def __getFilters(request):
    if SEARCH_SESSION in request.session.keys():
        searchData = request.session[SEARCH_SESSION]
        return searchData['search'], searchData['searchAuthor']
    return '', ''


def __get_paginated_objects(objects , page, pages):
    paginator = Paginator(objects, pages)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

def __clean_session(request):
    request.session.pop(SEARCH_SESSION, None)

class PostDelete(DeleteView):
    model = Message
    success_url = reverse_lazy('board:index')