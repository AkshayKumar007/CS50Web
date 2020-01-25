from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request,"login_auth/index.html")

def register_view(request):
    if request.method == "GET":
        return render(request, "login_auth/register.html")
    elif request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        uname = request.POST["uname"]
        passwd = request.POST["passwd"] 
        try:
            resp1 = User.objects.get(email=email)
        except:
            resp1 = None
        try:
            resp2 = User.objects.get(username=uname)
        except:
            resp2 = None
        if resp1 is not None:
            return JsonResponse({"message":"no_email"})
        elif resp2 is not None:
            return JsonResponse({"messsage":"no_name"})
        else:
            try:
                u = User.objects.create_user(username=uname, first_name=fname, last_name=lname,email=email, password=passwd)
                u.save()
                return JsonResponse({"message":"success"})
            except:
                return JsonResponse({"message":"wrong"})

def login_view(request):
    if request.method == "GET":
        return render(request,"login_auth/login.html")
    elif request.method == "POST":
        uname = request.POST["uname"]
        passwd = request.POST["passwd"]
        user = authenticate(request, username=uname, password=passwd)
        if user is not None:
            login(request, user)
            return JsonResponse({"message":"success"})  # may need to change
        else:
            return JsonResponse({"message":"wrong"})

@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect(index)
