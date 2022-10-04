import random
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        if request.POST['password'] == request.POST['cpassword']:
            password = request.POST['password']
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











# devv00973@gmail.com
# jzjeoafbfzxmmgur

