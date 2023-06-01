from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "authentication/login_page.html")


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def home(request):
    return render(request,"authentication/index.html")


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signup(request):
    
    if request.method == 'POST':
        
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        cpassword=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('signup')
            
    
        if User.objects.filter(email=email):
            messages.error(request, "email already exist!")
            return redirect('signup')
            
        
        if len(username)>10:
            messages.error(request, "Username contain lessthan 10 characters")
            return redirect('signup')

        if pass1!=cpassword:
            messages.error(request, "password didn't match")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric!")
            return redirect('signup')
        
        if not fname.strip():
            messages.error(request, "firstname must be alpha numeric!")
            return redirect('signup')
        
        if not lname.strip():
            messages.error(request, "Lastname must be alpha numeric!")
            return redirect('signup')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request, "Your account is created")
        return redirect('home')
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, "authentication/sign_up.html")


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signin(request):

    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass1']

        user = authenticate(request,username=username, password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('index')
    
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, "authentication/login_page.html")


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return HttpResponseRedirect("/")


