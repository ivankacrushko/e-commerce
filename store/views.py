from django.views.generic import ListView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
import sqlite3
import xml.etree.ElementTree as ET

from .models import *
from .forms import UserRegisterForm
from . utils import cookieCart, cartData, guestOrder



def productdetail(request,pk):
    is_admin = request.user.is_superuser
    product = Product.objects.get(id = pk)
    return render(request, 'store/product.html', {'product': product,'is_admin':is_admin})

def store(request):
    is_admin = request.user.is_superuser

    data = cartData(request)
    cartItems = data['cartItems']    
    products = Product.objects.all()

    context = {'products': products,'is_admin':is_admin, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    is_admin = request.user.is_superuser

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']  

    context = {'items':items, 'order':order,'is_admin':is_admin, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    is_admin = request.user.is_superuser

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items, 'order':order,'is_admin':is_admin, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    is_admin = request.user.is_superuser
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']    

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity += 1
        messages.success(request, "Pomyślnie dodano produkt do koszyka")
    elif action == 'remove':
        orderItem.quantity -= 1
        messages.success(request, "Pomyślnie usunięto produkt z koszyka")

    if orderItem.quantity <= 0:
        orderItem.delete()
    else:
        orderItem.save()
    
    return JsonResponse('Dodano produkt do koszyka', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
       customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id
    print(f"Total:{total}")
    print(f"order_total:{order.get_cart_total}")
    if float(total) == float(order.get_cart_total):
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            phone_number=data['shipping']['phone'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Płatność zakończona', safe=False)

def login(request):
    is_admin = request.user.is_superuser

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("posts:list")
    else:
        form = AuthenticationForm()          
    context = {'form': form, 'is_admin': is_admin}
    return render(request, 'store/login.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'store/logout.html')

def admin_site(request):
    is_admin = request.user.is_superuser
    context = {'is_admin': is_admin}
    return render(request, context, 'store/login.html')

def register(request):
    is_admin = request.user.is_superuser

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()            
            post_save.connect(create_customer_profile, sender=User)
            messages.success(request, "Twoje konto zostało utworzone pomyślnie")
            return redirect('store')
        else:
            messages.error(request, "Error")
    else:
        form=UserRegisterForm()

    context = {'form': form, 'is_admin': is_admin}    
    return render(request, 'store/register.html', context)

def passreset(request):
    is_admin = request.user.is_superuser
    
    return render(request, 'store/pass-reset.html', {'is_admin': is_admin})

def about(request):
    is_admin = request.user.is_superuser
    
    return render(request, 'store/about.html', {'is_admin': is_admin})

def contact(request):
    is_admin = request.user.is_superuser
    
    return render(request, 'store/contact.html', {'is_admin': is_admin})

def policy(request):

    is_admin = request.user.is_superuser
    
    return render(request, 'store/policy.html', {'is_admin': is_admin})

def ajax_search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)[:10]  # Limiting to 10 results
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url,
            })
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)



def export_db_to_xml(request):
    is_admin = request.user.is_superuser

    db_path = 'db.sqlite3'
    table_name = 'store_customer'
    xml_output_path = 'xml_customer.xml'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    root = ET.Element("database")
    table_element = ET.SubElement(root, table_name)
    
    for row in rows:
        row_element = ET.SubElement(table_element, "row")
        for col_name, col_value in zip(columns, row):
            col_element = ET.SubElement(row_element, col_name)
            col_element.text = str(col_value)
    
    tree = ET.ElementTree(root)
    with open(xml_output_path, "wb") as xml_file:
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    conn.close()
    return render(request, 'store/xml.html', {'is_admin': is_admin})

