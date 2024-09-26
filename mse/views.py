from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,request,HttpRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files import File 
#from user_agents import parse
from requests import request
import requests
import datetime
from django.core.mail import send_mail
from django.http.request import HttpRequest
from .models import *
#from .forms import *
import random,string,json,time
import smtplib
from email.mime.text import MIMEText



@login_required(login_url="/log-in/")
def get_username(request):
    return User.objects.get(id=request.user.id).username

@login_required(login_url="/log-in/")
def get_fullname(request):
    return Member.objects.get(username=User.objects.get(id=request.user.id).username).fullname

def generate_unique_id(s):
    id = s+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return id

def generate_otp():
    return str(random.randint(100000,999999))

def create_username(s):
    split_s = str(s).split("@")
    return split_s[0]

def validate_user(s):
    if User.objects.filter(username=s).exists():
        return True
    return False

def student_check(s):
    split_s = str(s).split("@")
    if split_s[1] == "ru.ac.bd":
        return True
    else:
        return False

def send_email(subject,body,receiver):
    sender = "teammaterialscience@gmail.com"
    password = "qtnobmvbodgautyf"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, receiver, msg.as_string())
    return True

def home(request):
    return render(request,"mse/home.html")

def terms(request):
    return render(request,"mse/terms.html")

def privacy(request):
    return render(request,"mse/privacy.html")

def about(request):
    return render(request,"mse/about.html")

def blogs(request,pk):
    if pk=="All":
        blogs = Blog.objects.all()
        cats = BlogCategory.objects.all()
    else:
        blogs = Blog.objects.filter(blog_category=pk)
        cats = BlogCategory.objects.filter(name=pk)
    category=pk
    context = {
        'blogs':blogs,
        'cats':cats,
        'category':category,
    }
    return render(request,"mse/blogs.html",context)

def blog(request,pk):
    blog = Blog.objects.get(blog_id=pk)
    comments = BlogComment.objects.filter(blog_id=pk)
    context = {
        'blog': blog,
        'comments':comments,
    }
    return render(request,"mse/blog.html",context)

@login_required(login_url="/log-in/")
def blog_like(request,pk):
    blog = Blog.objects.get(blog_id=pk)
    blog.total_likes = blog.total_likes + 1
    blog.save()
    return redirect("blog",pk)

@login_required(login_url="/log-in/")
def blog_comment(request,pk):
    if request.method == "POST":
        comment_body = request.POST.get("ans")
        userimage = File(Member.objects.get(username=get_username(request)).userimage,Member.objects.get(username=get_username(request)).userimage.name)
        comment = BlogComment.objects.create(comment_id=generate_unique_id("comment"),blog_id=pk,username=get_username(request),fullname=get_fullname(request),userimage=userimage,comment_body=comment_body)
        comment.save()
        blog = Blog.objects.get(blog_id=pk)
        blog.total_comments += 1
        blog.save()
        return redirect("blog",pk)
    return redirect("blog",pk)

@login_required(login_url="/log-in/")
def reply_comment(request,pk):
    if request.method == "POST":
        reply_comment_body = request.POST.get("ans")
        userimage = File(Member.objects.get(username=get_username(request)).userimage,Member.objects.get(username=get_username(request)).userimage.name)
        main_comment = BlogComment.objects.get(comment_id=pk)
        bid = main_comment.blog_id
        comment_reply = CommentReply.objects.create(reply_comment_id=generate_unique_id("recomment"),comment_id=main_comment,username=get_username(request),fullname=get_fullname(request),userimage=userimage,reply_comment_body=reply_comment_body)
        comment_reply.save()
        return redirect("blog",bid)

@login_required(login_url="/log-in/")
def delete_comment(request,pk):
    comment = BlogComment.objects.get(comment_id=pk)
    bid = comment.blog_id
    blog = Blog.objects.get(blog_id=bid)
    blog.total_comments = blog.total_comments - 1
    blog.save()
    comment.delete()
    return redirect("blog",bid)

@login_required(login_url="/log-in/")
def edit_reply_comment(request,pk):
    comment_reply = CommentReply.objects.get(reply_comment_id=pk)
    comment_reply.reply_comment_body = request.POST.get("ans")
    main_comment = comment_reply.comment_id
    bid = main_comment.blog_id
    return redirect("blog",bid)

@login_required(login_url="/log-in/")
def delete_reply_comment(request,pk):
    comment_reply = CommentReply.objects.get(reply_comment_id=pk)
    main_comment = comment_reply.comment_id
    bid = main_comment.blog_id
    comment_reply.delete()
    return redirect("blog",bid)

def books(request,pk):
    if pk=="All":
        books = Book.objects.all()
        cats = BookCategory.objects.all()
    else:
        books = Book.objects.filter(book_category=pk)
        cats = BookCategory.objects.filter(name=pk)
    category=pk
    context = {
        'books':books,
        'cats':cats,
        'category':category,
    }
    return render(request,"mse/books.html",context)

@login_required(login_url="/log-in/")
def mselanding(request):
    member = Member.objects.get(username=get_username(request))
    sems = Semester.objects.all()
    teachers = Teacher.objects.all()
    context = {
        'member':member,
        'sems':sems,
        'teachers':teachers,
    }
    return render(request,"mse/mselanding.html",context)

@login_required(login_url="/log-in/")
def mselanding2(request,pk):
    sem = Semester.objects.get(sem_id=pk)
    courses = Course.objects.filter(sem_id=pk)
    context = {
        'sem':sem,
        'courses':courses,
    }
    return render(request,"mse/mselanding2.html",context)

@login_required(login_url="/log-in/")
def mselanding3(request,pk):
    resources = Resource.objects.filter(course_code=pk)
    course_code = pk
    context = {
        'resources':resources,
        'course_code':course_code,
    }
    return render(request,"mse/mselanding3.html",context)

@login_required(login_url="/log-in/")
def uploadresource(request):
    if request.method == "POST":
        sem_id = request.POST.get("semester")
        course_code = request.POST.get("course")
        file = request.FILES["file"]
        name = file.name
        size = str(round(file.size/1048576,2))
        resource = Resource.objects.create(sem_id=sem_id,course_code=course_code,file=file,name=name,size=size)
        resource.save()
        return mselanding(request)
    sems = Semester.objects.all()
    courses = Course.objects.all()
    context = {
        'sems':sems,
        'courses':courses,
    }
    return render(request,"mse/uploadresource.html",context)

def odf(request):
    qs = Question.objects.all()
    context = {
        'qs':qs,
    }
    return render(request,"mse/odf.html",context)

@login_required(login_url="/log-in/")
def answer_question(request,pk):
    if request.method == "POST":
        ans = request.POST.get("ans")
        userimage = File(Member.objects.get(username=get_username(request)).userimage,Member.objects.get(username=get_username(request)).userimage.name)
        answer = Answer.objects.create(answer_id=generate_unique_id("ans"),question_id=pk,username=get_username(request),fullname=get_fullname(request),userimage=userimage,answer_description=ans)
        answer.save()
        question = Question.objects.get(question_id=pk)
        question.total_answer += 1
        question.save()
        return redirect("odfq",pk)

@login_required(login_url="/log-in/")
def reply_answer(request,pk):
    if request.method == "POST":
        ans = request.POST.get("ans")
        userimage = File(Member.objects.get(username=get_username(request)).userimage,Member.objects.get(username=get_username(request)).userimage.name)
        main_answer = Answer.objects.get(answer_id=pk)
        answer = AnswerReply.objects.create(reply_answer_id=generate_unique_id("ans"),answer_id=main_answer,username=get_username(request),fullname=get_fullname(request),userimage=userimage,reply_answer_description=ans)
        answer.save()
        pk2 = Answer.objects.get(answer_id=pk).question_id
        return redirect("odfq",pk2)

@login_required(login_url="/log-in/")
def edit_reply_answer(request,pk):
    if request.method == "POST":
        #qid = Answer.objects.get(answer_id=AnswerReply.objects.get(reply_answer_id=pk).answer_id).question_id
        reply_answer = AnswerReply.objects.get(reply_answer_id=pk)
        reply_answer.reply_answer_description = request.POST.get("ans")
        reply_answer.save()
        answer_object = reply_answer.answer_id
        qid = answer_object.question_id
        return redirect("odfq",pk=qid)

@login_required(login_url="/log-in/")
def delete_answer(request,pk):
    #qid = Answer.objects.get(answer_id=AnswerReply.objects.get(reply_answer_id=pk).answer_id).question_id
    answer = Answer.objects.get(answer_id=pk)
    qid = answer.question_id
    answer.delete()
    question = Question.objects.get(question_id=qid)
    question.total_answer -= 1
    question.save()
    return redirect("odfq",pk=qid)

@login_required(login_url="/log-in/")
def delete_reply_answer(request,pk):
    #qid = Answer.objects.get(answer_id=AnswerReply.objects.get(reply_answer_id=pk).answer_id).question_id
    reply_answer = AnswerReply.objects.get(reply_answer_id=pk)
    answer_object = reply_answer.answer_id
    qid = answer_object.question_id
    reply_answer.delete()
    return redirect("odfq",pk=qid)

@login_required(login_url="/log-in/")
def yourq(request):
    qs = Question.objects.filter(username=get_username(request))
    context = {
        'qs':qs,
    }
    return render(request,"mse/yourq.html",context)


def odfq(request,pk):
    q = Question.objects.get(question_id=pk)
    answers = Answer.objects.filter(question_id=pk)
    context = {
        'q':q,
        'answers':answers,
    }
    return render(request,"mse/odfq.html",context)

@login_required(login_url="/log-in/")
def askq(request):
    if request.method == "POST":
        question_title = request.POST.get("qtitle")
        question_description = request.POST.get("qtext")
        ques = Question.objects.create(question_id=generate_unique_id("ques"),question_title=question_title,question_description=question_description,username=get_username(request))
        ques.save()
    return render(request,"mse/askq.html")

def sign_in(request):
    if request.method == "POST":
        fullname = request.POST.get("name")
        email = request.POST.get("email")
        userimage = request.FILES["file"]
        password = request.POST.get("password")
        username = create_username(email)
        ru = student_check(email)
        valid = validate_user(username)
        if valid:
            return render(request,"mse/log-in.html",context={'message':"User already exists",})
        else:
            member = Member.objects.create(username=username,userimage=userimage,email=email,password=password,fullname=fullname,ru=ru)
            member.save()
            subject = "Verify your OTP"
            otp = generate_otp()
            request.session["otp"] = otp
            body = "Use this code to finish your registration : " + otp
            send = send_email(subject,body,email)
            if send:
                return redirect("otp",pk=email)
    return render(request,"mse/sign-in.html")

def verify_otp(request,pk):
    if request.method == "POST":
        entered_otp = str(request.POST.get("otpcode"))
        stored_otp = request.session.get("otp")
        if entered_otp == stored_otp:
            username = create_username(pk)
            password = Member.objects.get(username=username).password
            member = Member.objects.get(username=username)
            member.verified = True
            member.save()
            user = User.objects.create_user(username=username,password=password)
            user.save()
            auth_login(request,user)
            return redirect("odf")
        else:
            return render(request,"mse/verify-otp.html",{'message': 'OTP did not match!','pk':pk})
    return render(request,"mse/verify-otp.html",{'pk':pk})

def resend_otp(request,pk):
    if request.method == "POST":
        entered_otp = str(request.POST.get("otpcode"))
        stored_otp = request.session.get("otp")
        if entered_otp == stored_otp:
            username = create_username(pk)
            password = Member.objects.get(username=username).password
            member = Member.objects.get(username=username)
            member.verified = True
            member.save()
            user = User.objects.create_user(username=username,password=password)
            user.save()
            auth_login(request,user)
            return redirect("odf")
        else:
            return render(request,"mse/sign-in.html",{'message': 'OTP did not match!'})
    

    subject = "Verify your OTP"
    otp = generate_otp()
    request.session["otp"] = otp
    body = "Use this code to finish your registration : " + otp
    send = send_email(subject,body,pk)
    if send:
        return redirect("otp",pk=pk)

def log_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = create_username(email)
        password = request.POST.get("password")
        try:
            if password == Member.objects.get(username=username).password:
                user = User.objects.get(username=username)
                auth_login(request,user)
                return redirect("odf")
            else:
                return render(request,"mse/log-in.html",{'message':'Password did not match!'})
        except:
            return render(request,"mse/log-in.html",{'message':'Username & password did not match!'})
    return render(request,"mse/log-in.html")

def sign_out(request):
    logout(request)
    return redirect("home")

def forgot(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not Member.objects.filter(username=create_username(email)).exists():
            return render(request,"mse/forgot.html",{'message':'You do not have account! Please Sign In!'})
        else:
            subject = "Verify your OTP"
            otp = generate_otp()
            request.session["otp"] = otp
            body = "Use this code to reset your password : " + otp
            send_email(subject,body,email)
            return redirect("forgotpass",email)
    return render(request,"mse/forgot.html")

def forgot_password(request,pk):
    if request.method == "POST":
        entered_otp = str(request.POST.get("otpcode"))
        stored_otp = request.session.get("otp")
        if entered_otp == stored_otp:
            return redirect("resetpass",pk)
        else:
            return render(request,"mse/forgotpass.html",{'message':'OTP did not match','email':pk,})
    return render(request,"mse/forgotpass.html",{'email':pk})

def reset_password(request,pk):
    if request.method == "POST":
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        if pass1==pass2:
            member = Member.objects.get(username=create_username(pk))
            member.password = pass1
            member.save()
            user = User.objects.get(username=create_username(pk))
            user.password = pass1
            user.save()
            return redirect("log-in")
        else:
            return render(request,"mse/reset.html",{'email':pk,'message':'Password did not match'})
    return render(request,"mse/reset.html",{'email':pk})