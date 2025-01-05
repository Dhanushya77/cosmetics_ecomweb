from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from.models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.

def cosmetic_login(req):
    if 'shop' in req.session:
        return redirect (shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        shop = authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            if shop.is_superuser:
                req.session['shop'] = uname
                return redirect(shop_home)
            else:
                req.session['user'] = uname
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password')
            return redirect(cosmetic_login)
    else:
        return render(req,'login.html')
    

#-----------------admin----------------------------------------


def cosmetic_logout(req):
    logout(req)
    req.session.flush()
    return redirect(cosmetic_login)

def shop_home(req):
    if 'shop' in req.session:
        # products = product.objects.all()
        categories = Category.objects.all()
        category_products = {category.category: product.objects.filter(category=category) for category in categories}
        details = Details.objects.all()
        return render(req,'shop/home.html',{'details':details,'category':categories,"category_products":category_products})
    else:
        return redirect(cosmetic_login)
    

def category(req):
    if req.method=='POST':
        category=req.POST['category']
        data= Category.objects.create(category=category)
        data.save()
        return redirect(view_category)
    else:
        data=Category.objects.all()
        return render(req,'shop/category.html',{'data':data})

def view_category(req):
    category=Category.objects.all()
    return render(req,'shop/view_category.html',{'category':category})
    
def delete_category(req,id):
    data=Category.objects.get(pk=id)
    data.delete()
    return redirect(view_category)

def view_products(req,id):
    category = Category.objects.get(pk=id)
    details = Details.objects.filter(product__category=category)
    return render(req, 'shop/view_products.html', {'category': category,'details': details})
 

    
def add_pro(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            pid = req.POST['pid']
            name = req.POST['name']
            dis = req.POST['dis']
            category = req.POST['category']
            img = req.FILES.get('img')
            data = product.objects.create(pid=pid,name=name,dis=dis,category=Category.objects.get(category=category),img=img)
            data.save()
            return redirect(details)
        else:
            data=Category.objects.all()
            return render(req,'shop/add_pro.html',{'data':data})
    else:
        return redirect(cosmetic_login)
    
def details(req):
    if req.method=='POST':
        pro=req.POST['pid']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        weight=req.POST['weight']
        product_instance = product.objects.get(pid=pro)
        data=Details.objects.create(price=price,offer_price=offer_price,stock=stock,weight=weight,product=product_instance)
        data.save()
        return redirect(shop_home)

    else:
        data=product.objects.all()
        return render(req,'shop/details.html',{'data':data})
    
    
def edit_pro(req, id):
    if req.method == 'POST':
        pid = req.POST['pid']
        name = req.POST['name']
        dis = req.POST['dis']
        price = req.POST['price']
        offer_price = req.POST['offer_price']
        stock = req.POST['stock']
        weight = req.POST['weight']
        img = req.FILES.get('img')
        product_data = product.objects.get(pk=id)
        if img:
            product.objects.filter(pk=id).update(pid=pid, name=name, dis=dis)
            data = product.objects.get(pk=id)
            data.img = img
            data.save()
        else:
            product.objects.filter(pk=id).update(pid=pid, name=name, dis=dis)
        
        Details.objects.filter(product=product_data).update(price=price, offer_price=offer_price, stock=stock,weight=weight)
        return redirect(shop_home)
    else:
        product_data = product.objects.get(pk=id)
        details_data = Details.objects.get(product=product_data)
        return render(req, 'shop/edit_pro.html', {'product_data': product_data, 'details_data': details_data})

    
def delete_pro(req,pid):
    data=product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)



# -----------------user---------------------------------------------

def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswrd=req.POST['pswrd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswrd)
            data.save()
            otp=""
            for i in range(6):
                otp+=str(random.randint(0,9))
            msg=f'Your registration is completed otp: {otp}'
            otp=Otp.objects.create(user=data,otp=otp)
            otp.save()
            send_mail('Registration',msg, settings.EMAIL_HOST_USER, [email])
            return redirect(otp_confirmation)
        except:
            messages.warning(req,'Email already exist')
            return redirect(register)
    else:
        return render(req,'user/register.html')
    
def otp_confirmation(req):
    if req.method == 'POST':
        uname = req.POST.get('uname')
        user_otp = req.POST.get('otp')
        try:
            user = User.objects.get(username=uname)
            generated_otp = Otp.objects.get(user=user)
    
            if generated_otp.otp == user_otp:
                generated_otp.delete()
                return redirect(cosmetic_login)
            else:
                messages.warning(req, 'Invalid OTP')
                return redirect(otp_confirmation)
        except User.DoesNotExist:
            messages.warning(req, 'User does not exist')
            return redirect(otp_confirmation)
        except Otp.DoesNotExist:
            messages.warning(req, 'OTP not found or expired')
            return redirect(otp_confirmation)
    return render(req, 'user/otp.html')

    
def user_home(req):
    if 'user' in req.session:
        products = product.objects.all().order_by('id')
        category=Category.objects.all()
        return render(req,'user/home.html',{'product':products,'category':category})
    else:
        return redirect(cosmetic_login)

def view_details(req,id):
    products = product.objects.filter(pk=id).first()
    data=Details.objects.all()
    if products:
        details = Details.objects.filter(product=products).first()
        
        if details:
            return render(req,'user/view_details.html',{'details':details,'data':data})
        else:
            
            return render(req,'user/view_details.html', {'message': 'No details available for this product.'})
    else:
        
        return render(req, 'user/view_details.html', {'message': 'Product not found.'})

def add_to_cart(req, pid):
    products = product.objects.filter(pk=pid).first()
    details = Details.objects.get(product=products)
    user = User.objects.get(username=req.session['user'])
    try:
        cart = Cart.objects.get(details=details, user=user)
        cart.quantity += 1
        cart.save()
    except:
        data = Cart.objects.create(details=details, user=user, quantity=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user = User.objects.get(username=req.session['user'])
    data = Cart.objects.filter(user=user)
    total_price = sum(item.quantity * item.details.offer_price for item in data)
    return render(req, 'user/cart.html', {'cart': data,'total_price':total_price})


def quantity_inc(req,cid):
    data=Cart.objects.get(pk=cid)
    if data.details.stock > data.quantity:
        data.quantity+=1
        data.save()
    return redirect(view_cart) 

def quantity_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.quantity-=1
    data.save()
    if data.quantity==0:
        data.delete()
    return redirect(view_cart)

def buy_pro(req,pid):
    products=product.objects.filter(pk=pid).first()
    details=Details.objects.get(product=products)
    user=User.objects.get(username=req.session['user'])
    quantity=1
    price=details.offer_price
    buy=Buy.objects.create(details=details,user=user,quantity=quantity,t_price=price)
    buy.save()
    return redirect(user_bookings)

def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    bookings=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/user_bookings.html',{'bookings':bookings})

def cart_buy(req):
    user = User.objects.get(username=req.session['user'])
    cart_items = Cart.objects.filter(user=user)

    if not cart_items:
        return redirect(view_cart)

    for cart in cart_items:
        price = cart.quantity * cart.details.offer_price
        details = cart.details

        if details.stock >= cart.quantity:

            details.stock -= cart.quantity
            details.save()

            Buy.objects.create(details=details,user=user,quantity=cart.quantity,t_price=price)
        else:
            return redirect(view_cart)

    # cart_items.delete()

    # return redirect(user_bookings)

def filter_products(req):
    category=Category.objects.all()
    return render(req,'shop/view_category.html',{'category':category})

def view_filtered(req,id):
    category = Category.objects.get(pk=id)
    details = Details.objects.filter(product__category=category)
    return render(req, 'user/filter.html', {'category': category,'details': details})
   