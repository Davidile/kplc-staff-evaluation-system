from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import Signupform, Add_record
from .models import Record

# Create your views here.
def landing_page(request):
    return render(request,"index.html")

def home(request):
    records=Record.objects.all()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have logged in successfully")
            return redirect('home')
        else:
            messages.success(request,"There was an error please login again")
            return redirect('home')
    return render(request,"home.html",{'records':records})

def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request,'you have logged out')
    return redirect('home')

def register_user(request):
    if request.method=="POST":
        form=Signupform(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"you have successfull registered")
            return redirect('home')
    else:
        form=Signupform()
        return render(request,"register.html",{'form':form})
    return render(request,"register.html",{'form':form})

def record(request,pk):
    if request.user.is_authenticated:

       customer_record=Record.objects.get(id=pk)
       return render(request,"record.html",{'customer_record':customer_record})
    else:
        messages.success(request,"You must be logged in !")
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
      delete_it=Record.objects.get(id=pk)
      delete_it.delete()
      messages.success(request,"Records deleted successfully....")
      return redirect('home')
    else:
        messages.success(request,"You must be logged in to do that!")
        return redirect('home')



def add_record(request):
    form=Add_record(request.POST or None)
    if request.user.is_authenticated:
       if request.method=="POST":  
            if form.is_valid():
              form.save()
              messages.success(request,"Records added successfully ...")
              return redirect('home')
         
       return render(request,"add_record.html",{'form':form})
    else:
        messages.success(request,"You must be logged in ..")
        return redirect("home")
    

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form=Add_record(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been updated")
            return redirect("home")
        return render(request,"update_record.html",{'form':form})
    else:
         messages.success(request,"You must be logged in ..")
         return redirect("home")
    


