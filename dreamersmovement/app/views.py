from django.shortcuts import render,redirect
from .models import contact,joiners
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login as user_login, logout as user_logout

# Create your views here.
vrcode = None
def Home(request):
    global vrcode 
    vrcode = None
    if request.method == "POST":
        if request.POST.get('message-c'):
            namec = request.POST.get('name-c')
            emailc = request.POST.get('email-c')
            phonec = request.POST.get('phone-c')
            messagec = request.POST.get('message-c')
            user = contact()
            user.name = namec
            user.email = emailc
            user.phone = phonec
            user.message = messagec
            user.save()
            return  redirect('/')
        else:
            namej = request.POST.get('name')
            phonej = request.POST.get('number')
            classj = request.POST.get('class')
            emailj = request.POST.get('email')
            user =  joiners()
            user.name = namej
            user.phone = phonej
            user.clas = classj
            user.email = emailj
            user.save()
            return redirect('/')
        
    return render(request,'index.html')

def Login(request):
    global vrcode
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
       if request.POST.get('email'):
           global users,emails,passwords
           users = request.POST['username']
           emails = request.POST['email']
           passwords = request.POST['password']
           if User.objects.filter(email=emails).exists() or User.objects.filter(username=users).exists():
               error = {
                   'message':'The username or the email you entered already exists'
               }
               return render(request,'index-l.html', error)
           else:
                vrcode = random.randrange(100000, 1000000)
                emails = str(emails)
                subject = 'Email verification'
                message = f'your verification code is {vrcode}'
                from_email = 'mohammadhadimalik@gmail.com'
                recipient_list = [emails]
                send_mail(subject, message, from_email, recipient_list)
                return redirect('/vr')
       else:
           userl = request.POST['username']
           passl = request.POST['password']
           user_auth_check = authenticate(request,username=userl,password=passl)
           if user_auth_check == None:
               error = {
                   'message':'the email or password you entered is incorrect'
               }
               return render(request,'index-l.html', error)
           else:
               user_login(request,user_auth_check)
               print("user login hova")
               return redirect('/')
    return render(request,'index-l.html')

def vr(request):
    global vrcode
    if request.user.is_authenticated:
        return redirect('/')
    if vrcode is None:
        return redirect('/')
    if request.method == 'POST':
        print('yahan tak chala')
        user_input = request.POST['code']
        print("yahan bhi")
        print(user_input,vrcode)
        if int(user_input) == int(vrcode):
            print("yahan bhi2")
            global user
            user = User.objects.create_user(username=users,email=emails,password=passwords)
            user.save()
            print('userbana')
            vrcode = None
            success = {
                   'success':'Account Created Successfully please login'
               }
            return render(request,'index-l.html', success)
        else:
            vrm = {
                'vrcodeerror':"please enter the correct value"
            }
            return render(request,'vr.html',vrm)

    return render(request,'vr.html')


def logout(request):
    user_logout(request)
    return redirect('/')