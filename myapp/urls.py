from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register , name='register'),
    path('otp/', views.otp, name='otp'),
    path('login/', views.login, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_blog', views.add_blog, name="add_blog"),
    path('my_blog', views.my_blog, name="my_blog"),
    path('view_blog', views.view_blog, name="view_blog"),
    path('donate/<int:pk>', views.donate, name="donate"),







    
]