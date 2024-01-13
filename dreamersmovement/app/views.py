from django.shortcuts import render,redirect
from .models import contact,joiners,donaters
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
import razorpay

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



def donate(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        global named,addressd,amountd,payment
        named = request.POST['named']
        addressd = request.POST['addressd']
        amountd = request.POST['amountd']
        client = razorpay.Client(auth=("rzp_test_RkzDSuQFA1u5aO", "POhTCz7Vv93f27YrMRzsyqwR"))
        data = { "amount": int(amountd) *100, "currency": "INR" ,'payment_capture':1 }
        payment = client.order.create(data=data) 
        print(payment)
        return render(request, 'index-d.html', {'payment':payment})   
    return render(request,'index-d.html')

def success(request):
    global payment,user
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        if not request.GET.get('razorpay_payment_id'):
            return redirect('/')
        if not request.GET.get('razorpay_order_id'):
            return redirect('/')
        if not request.GET.get('razorpay_signature'):
            return redirect('/')
        if not request.GET.get('razorpay_order_id') == payment['id']:
            return redirect('/')
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_order_id = request.GET.get('razorpay_order_id')
        razorpay_signature = request.GET.get('razorpay_signature')

        donater = donaters(named = named,addressd=addressd,amountd=amountd, emaild = request.user.email, order_id=razorpay_order_id,payment_id=razorpay_payment_id,payment_signature=razorpay_signature)

        donater.save()
        subject = 'Heartfelt Gratitude for Your Generosity'
        message = f"""
        Subject: Heartfelt Gratitude for Your Generosity 💖

        Dear {request.user.username},

        I hope this message finds you well. We are thrilled and deeply grateful for your recent donation to [Organization/cause]. Your generosity is a shining beacon of support, and we cannot express how much it means to us.

        **Donation Details:**
        - **Amount:** [{amountd}]
        - **Payment ID:** [{razorpay_payment_id}]

        Your commitment to [describe the cause or initiative] is truly inspiring. With contributions like yours, we can continue [explain the impact of donations and how they contribute to the organization's mission].

        As a token of our appreciation, please find attached a [certificate/thank-you note] expressing our gratitude. Your name will also be featured prominently in our list of esteemed donors, recognizing the incredible difference you're making.

        **Next Steps:**
        Kindly check your email for a detailed receipt containing your payment ID and other relevant information. If you have any questions or require further assistance, feel free to reply to this email or contact us at [7889484343].

        Once again, thank you for your unwavering support. Together, we are creating positive change and making the world a better place.

        With sincere thanks,

        [Dreamers Movement]
        [7889484343]
        """

        from_email = 'mohammadhadimalik@gmail.com'
        recipient_list = [request.user.email]
        send_mail(subject, message, from_email, recipient_list)
        return render(request, 'success.html')