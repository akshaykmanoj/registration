from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'adminpanel/admin_login.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='admin_index')
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        member=User.objects.all()
        return render(request, 'adminpanel/admin_page.html', {'member':member})
    return render(request, 'adminpanel/admin_login.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')

        else:
            messages.error(request, "Invalid superuser credentials")
            return redirect("admin_login")

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')

    return render(request, 'adminpanel/admin_login.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add(request):
    return render(request, 'adminpanel/add.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_record(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        
        if not username.strip():
            messages.error(request, "Username is required")
            return redirect('add')

        if not fname.strip():
            messages.error(request, "First name is required")
            return redirect('add')

        if not lname.strip():
            messages.error(request, "Last name is required")
            return redirect('add')

        if not email.strip():
            messages.error(request, "Email is required")
            return redirect('add')


        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken')
            return redirect('add')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email address is already taken')
            return redirect('add')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, 'Your account has been successfully created.')
        return redirect('admin_dashboard')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update(request, id):
    member = User.objects.get(id = id)
    return render(request, 'adminpanel/update.html', {"member" : member})



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update_record(request, id):
    if request.method == "POST":
    
        fname = request.POST['fname'].strip()
        lname = request.POST['lname'].strip()
        username=request.POST['username'].strip()
        email=request.POST['email'].strip()

        member = User.objects.get(id = id)
    
        if not fname:
            messages.error(request, "First name is required")
            return redirect('update',id)

        if not lname:
            messages.error(request, "Last name is required")
            return redirect('update',id)
        
        if not username:
            messages.error(request, "username is required")
            return redirect('update',id)
        
        if not email:
            messages.error(request, "mail is required")
            return redirect('update',id)
        
        if username and username != member.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exist!")
                return redirect('update',id)
            member.username=username
            
        if email and email != member.email:   
            if User.objects.filter(email=email).exists():
                messages.error(request, "email already exist!")
                return redirect('update',id)
            member.email=email

        # myuser = User.objects.get(id = id)
        # myuser.first_name = fname
        # myuser.last_name = lname
        member.save()
        
        # myuser.save()
        return redirect('admin_dashboard')
    

@cache_control(no_cache=True,must_revalidate=True,no_store=True)    
def delete(request, id):
    member = User.objects.get(id = id)
    member.delete()
    return redirect('admin_dashboard')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            detail=User.objects.filter(username=query)
            return render(request,'adminpanel/search.html',{'details':detail})
        else:
            return render(request, 'adminpanel/search.html',{})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)    
def admin_signout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('admin_dashboard')