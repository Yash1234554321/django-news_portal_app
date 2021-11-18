import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from news_app.models import news

@login_required()
def index(request):
    db_news = news.objects.all()
    request.session.get("added_news")
    return render(request,"news_app/index.html",{"news":db_news,"current_user":request.user})

@login_required()
def add_news(request):
    if request.method == "GET":
        return render(request,"news_app/addnews.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        current_date = datetime.datetime.now().date()

        news_add = news.objects.create(title=title,content=content,date_posted=current_date,author_id=request.user.id)
        news_add.save()

        request.session["added_news"] = "News has been added."
        messages.success(request,"News has been added successfully.")
        return redirect("index")

@login_required()
def update_news(request,id):
    db_news = news.objects.get(id=id)
    if request.method == "GET":
        return render(request,"news_app/updatenews.html",{"news":db_news})
    else:
        db_news.title = request.POST["title"]
        db_news.content = request.POST["content"]
        db_news.save()

        return redirect("index")

@login_required()
def delete_news(request,id):
    db_news = news.objects.get(id=id)
    db_news.delete()

    return redirect("index")

def contact(request):
    if request.method == "GET":
        return render(request,"news_app/contact.html")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        comment = request.POST["comment"]

        send_mail("Comment Sent Successfully",
                    "Your inquiry has been submitted successfully. Our representatives will contact ypu shortly.",
                    settings.EMAIL_HOST_USER,[email])
        
        send_mail("A query has been created",
                    f"{first_name} {last_name} {email}",
                    settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER])
        
        return redirect("index")

def profile(request):
    if request.method == "GET":
        return render(request,"profile.html",{"user_info":request.user})

def signup(request):
    if request.method == "GET":
        return render(request,"authentication/signup.html")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
        if user is not None:
            sub = "Account created"
            msg = f"Hello {first_name}. An account has been created for you successfully. Your username is {username}."
            email_from = settings.EMAIL_HOST_USER
            email_to = [email]
            send_mail(sub,msg,email_from,email_to)
            return redirect("signin")
        else:
            return redirect("signup")

def signin(request):
    if request.method == "GET":
        return render(request,"authentication/signin.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            url = request.GET.get("next")
            if url is not None:
                return redirect(url)
            else:
                return redirect("index")
        else:
            messages.error(request,"Invalid username and password.")
            messages.error(request,"Please check your credentials and try again.")
            return redirect('signin')

def signout(request):
    logout(request)
    return redirect("index")

@login_required()
def reset_password(request):
    if request.method == "GET":
        return render(request,"authentication/reset_password.html")
    else:
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]

        user = authenticate(request,username=request.user.username,password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            return redirect("index")
        else:
            return redirect("reset_password")