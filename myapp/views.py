import random
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from myapp.models import Blog, User
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
    return HttpResponse('Done!!')



# devv00973@gmail.com
# jzjeoafbfzxmmgur

