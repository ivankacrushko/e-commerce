from django.urls import path

from django.urls import path
from django.shortcuts import redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('login/', auth_views.LoginView.as_view(template_name="store/login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_site/', lambda request: redirect('/admin/'), name='admin_site'),
    path('register/', views.register, name='register'),
    path('pass-reset/', views.passreset, name='passreset'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policy/', views.policy, name='policy'),
    path('products/<int:pk>/', views.productdetail, name='productdetail'),
    path('xml/', views.export_db_to_xml, name='xml'),
    path('ajax/search/', views.ajax_search, name='ajax_search'),
]