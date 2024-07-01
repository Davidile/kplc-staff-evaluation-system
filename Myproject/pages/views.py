from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import PerformanceReviewForm
from .models import PerformanceReview
from django.http import HttpResponse
from .models import PerformanceReview
from django.db.models import F, Value, FloatField
from django.db.models.functions import Coalesce
from weasyprint import HTML
from django.template.loader import render_to_string,get_template




# Create your views here.
def landing_page(request):
    return render(request,"base.html")

def home(request):
    if request.user.is_authenticated:
       reviews = PerformanceReview.objects.filter(user=request.user)
      # reviews = PerformanceReview.objects.all()
       return render(request, "home.html", {'reviews': reviews})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully")
                return redirect('home')
            else:
                messages.error(request, "There was an error, please try again")
                return render(request, 'home.html')
        return render(request, "home.html")
  
def logout_user(request):
    logout(request)
    messages.success(request,'you have logged out')
    return redirect('landing_page')


"""def register_user(request):
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
    
"""

def add_performance_review(request):
 if request.user.is_authenticated:
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            performance_review = form.save(commit=False)
            performance_review.user = request.user
            if not performance_review.can_review():
                messages.error(request,"user has been reviewed in the last 120days.")
                return redirect('home')
            performance_review.save()
            messages.success(request,'review added successfully')
            return redirect('home')
    else:
        form = PerformanceReviewForm()
    return render(request, 'home.html', {'form': form})
 
def track_progress(request):
    reviews = PerformanceReview.objects.all()
    sorted_reviews = sorted(reviews, key=lambda review: review.calculate_total_score(), reverse=True)
    return render(request, 'track_progress.html', {'reviews': sorted_reviews})


def generate_pdf(request):
    reviews = PerformanceReview.objects.all()
    sorted_reviews = sorted(reviews, key=lambda review: review.calculate_total_score(), reverse=True)
    template = get_template('generatepdf.html')
    html = template.render({'reviews': sorted_reviews})

    pdf = HTML(string=html,base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline;attachment; filename="performance_report.pdf"'

    return response