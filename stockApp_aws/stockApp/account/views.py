import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import account
from account.forms import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm
from post.models import Post
from account.models import Account

from operator import attrgetter

# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            rawpassword = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=rawpassword)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)




def logout_view(request):
    logout(request)
    return redirect('home')



def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")
    
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, 'account/login.html', context)


def account_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    
    else:
        form = AccountUpdateForm(
            initial = {
                "username": request.user.username,
                "email": request.user.email,
                'fullname': request.user.fullname,
                "bio": request.user.bio,
            }
        )
    
    context['account_form'] = form
    return render(request, 'account/account.html', context)




def profile_view(request, username):
    # user = request.user
    # if not user.is_authenticated:
    #     return redirect("home")

    user = Account.objects.filter(username=username)
    user = user[0]
    date_joined = user.date_joined.strftime("%b %d, %Y")
    month, day, year = date_joined.split()
    if day[0] == '0':
        day = day[1] + ','
    else:
        day += " "
    date_joined = month + " " + day + year
    usr = {
        'username': user.username,
        'fullname': user.fullname,
        'email': user.email,
        'date_joined': date_joined,
        'bio': user.bio,
    }
    
    trades = sorted(Post.objects.filter(author=user), key=attrgetter('date_published'), reverse=True)
    num_trades = len(trades)

    context = {
        "user": usr,
        "num_trades": num_trades,
        "trades": trades,
    }


    return render(request, 'account/profile.html', context)