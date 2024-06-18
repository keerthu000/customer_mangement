from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.genicpage,name='genicpage'),
    path('checkeregister',views.checkeregister,name='checkeregister'),
    # path('adminpage',views.adminpage,name=' adminpage'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('login_view',views.login_view,name='login_view',),
    path('add_checker',views.add_checker,name='add_checker'),
    
    path('maker_register',views.maker_register,name='maker_register'),
    path('add_maker_register',views.add_maker_register,name='add_maker_register'),
    path('checkerpage',views.checkerpage,name='checkerpage'),
    path('makerpage',views.makerpage,name='makerpage'),
    path('createcustomer',views.createcustomer,name='createcustomer'),
    path('create_profile',views.create_profile,name='create_profile'),
    path('customerdetails/<int:id>/',views.customerdetails,name='customerdetails'),
    path('genicpage',views.genicpage,name='genicpage'),
    path('showcustdetails/<int:id>/',views.showcustdetails,name='showcustdetails'),
    path('approve/<int:id>/',views.approve_customer, name='approve_customer'),
    path('reject/<int:id>/', views.reject_customer, name='reject_customer'),
]