import random
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from myapp.models import Blog, User
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# Create your views here.


def index(request):
    try:
        request.session['email']
        user = User.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'user_object': user})
    except:
        return render(request, 'login.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        if request.POST['password'] == request.POST['cpassword']:
            password = request.POST['password']
            global user_data
            user_data = {
                'first_name' : request.POST['fname'],
                'last_name' : request.POST['lname'],
                'email' : request.POST['email'],
                'mobile' : request.POST['mobile'],
                'password' : request.POST['password'],
                're_password' : request.POST['cpassword']
            }
            if len(password) >= 8 :
                special_char = False
                numbers = False
                upper_case = False
                lower_case = False
                for i in password:
                    if i in '!@#$%^&*':
                        special_char = True
                    if i in '0123456789':
                        numbers = True
                    if 97 <= ord(i) <= 122:
                        lower_case = True
                    if 65 <= ord(i) <= 90:
                        upper_case = True
                if lower_case and upper_case and special_char and numbers:
                    global c_otp
                    c_otp = random.randint(1000,9999)
                    subject = "Registration At Blogspot"
                    message = f"Your OTP is {c_otp}."
                    from_email = settings.EMAIL_HOST_USER
                    send_mail(subject, message, from_email, [request.POST['email']])
                    return render(request, 'otp.html', {'msg':'Check Your Inbox!!'})
                else:
                    return render(request, 'register.html', {'msg': 'akjsdklasjd'})
        else:
            return render(request, 'register.html', {'msg':'Both passwords are not same!!'})


def otp(request):
    if request.method == 'POST':
        if c_otp == int(request.POST['uotp']):
            User.objects.create(
                first_name = user_data['first_name'],
                last_name = user_data['last_name'],
                email = user_data['email'],
                mobile = user_data['mobile'],
                password = user_data['password']
            )
            return render(request, 'register.html', {'msg': 'Account Successfully created!!'})
    return render(request, 'login.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            global user
            user_object = user = User.objects.get(email = request.POST['email'])
            if user_object.password == request.POST['password']:
                request.session['email'] = request.POST['email']

                return render(request, 'index.html',{'user_object':user_object})
            else:
                return render(request, 'login.html', {'msg' : 'Wrong password!!'})
        except:
            return render(request, 'login.html', {'msg': 'Email Does Not Exist!!'})


def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')
    else:
        u_email = request.POST['email']
        try:
            user_object = User.objects.get(email = u_email)
            subject = 'Account Recovery'
            message = f'Your password is {user_object.password}.'
            from_email = settings.EMAIL_HOST_USER
            rec = [u_email]
            send_mail(subject, message, from_email, rec)
            return render(request, 'login.html')
        except:
            return render(request, 'forgot_password.html', {'msg':'Account does not exist!!!'})


def logout(request):
    del request.session['email']
    return render(request, 'login.html')

    
def edit_profile(request):
    try:
        user_object = User.objects.get(email = request.session['email'])
        if request.method == 'POST':
            user_object.first_name = request.POST['fname']
            user_object.last_name = request.POST['lname']
            user_object.mobile = request.POST['mobile']
            if request.FILES:
                user_object.pic = request.FILES['pic']
            user_object.save()
            return render(request, 'edit_profile.html',{'user_object':user_object})
        else:
            user_object = User.objects.get(email = request.session['email'])
            return render(request, 'edit_profile.html',{'user_object':user_object})
    except:
        return render(request, 'login.html')


def add_blog(request):
    if request.method == 'GET':
        return render(request, 'add_blog.html', {'user_object':user})
    else:
        user_object = User.objects.get(email = request.session['email'])
        Blog.objects.create(
            title = request.POST['title'],
            user = user_object,
            description = request.POST['description'],
            pic = request.FILES['pic']
        )
        return render(request, 'add_blog.html',  {'user_object':user})


def my_blog(request):
    user_object = User.objects.get(email = request.session['email'])
    blogs = Blog.objects.filter(user = user_object)
    return render(request, 'my_blog.html',{'blogs': blogs, 'user_object':user})


def view_blog(request):
    all_blogs = Blog.objects.all()
    return render(request, 'view_blog.html', {'all_blogs': all_blogs, 'user_object': user})


def donate(request, pk):
    #payment
    #donation table row create
    blog_object = Blog.objects.get(id = pk)
    currency = 'INR'
    amount = 4500*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    global context
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['single_blog'] = blog_object
    return render(request, 'donate.html', context = context)


 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


 

 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is not None:
            amount = context['razorpay_amount']  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                return render(request, 'paymentsuccess.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
            
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()




# devv00973@gmail.com
# jzjeoafbfzxmmgur

