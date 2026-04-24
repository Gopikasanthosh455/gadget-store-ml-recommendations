from django.shortcuts import render,redirect
from AdminApp.models import categoryDB, productDB, serviceDB
from WebApp.models import contactDB, sign_upDB, cartDB, checkoutDB, productViewEvent
from django.contrib import messages
from django.db.models import Count
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response

from WebApp.recommendations import get_recommended_products
from WebApp.serializers import ProductRecommendationSerializer

# Create your views here.
def _get_cart_context(request):
    username = request.session.get('Username')
    cart_count = cartDB.objects.filter(Username=username).count() if username else 0
    return username, cart_count


def _track_product_view(request, product):
    if not request.session.session_key:
        request.session.create()
    productViewEvent.objects.create(
        Username=request.session.get('Username'),
        session_key=request.session.session_key,
        product=product,
    )


def home_page(request):
    categories=categoryDB.objects.all()
    _, x = _get_cart_context(request)
    return render(request,"Home.html",{'categories':categories,"x":x})
def about_page(request):
    categories = categoryDB.objects.all()
    _, x = _get_cart_context(request)
    service = serviceDB.objects.all()
    return render(request,"About.html",{'categories':categories,'service':service,"x":x})
def product_page(request):
    categories = categoryDB.objects.all()
    products=productDB.objects.all()
    _, x = _get_cart_context(request)
    return render(request,"product.html",{'products':products,'categories':categories,"x":x})
def contact_page(request):
    categories = categoryDB.objects.all()
    _, x = _get_cart_context(request)
    return render(request,"contact.html",{'categories':categories,"x":x})
def filtered_page(request,cat_name):
    categories = categoryDB.objects.all()
    _, x = _get_cart_context(request)
    data=productDB.objects.filter(Category_name=cat_name)
    return render(request,"filtered_html.html",{'data':data,'categories':categories,"x":x})
def single_items(request,item_id):
    categories = categoryDB.objects.all()
    product=productDB.objects.get(id=item_id)
    _track_product_view(request, product)
    _, x = _get_cart_context(request)
    recommended_products = get_recommended_products(product.id, limit=4)
    return render(
        request,
        "single_items.html",
        {
            'product':product,
            'categories':categories,
            "x":x,
            "recommended_products": recommended_products,
        },
    )
def save_contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        obj=contactDB(Name=name,Email=email,Phone=phone,Message=message)
        obj.save()
        messages.success(request, "Thank you! We Contact you later..!")
        return redirect(contact_page)
def sign_in(request):
    return render(request,"sign_in.html")
def sign_up(request):
    return render(request,"sign_up.html")
def save_sign_up(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        email=request.POST.get('email')
        obj=sign_upDB(Username=username,Password=password,Confirm_password=password1,Email=email)
        obj.save()
        messages.success(request, "Registration successfully")
        return redirect(sign_in)
def user_login(request):
    if request.method=="POST":
        un=request.POST.get('username')
        pswd=request.POST.get('password')
        if sign_upDB.objects.filter(Username=un,Password=pswd).exists():
            request.session['Username']=un
            request.session['Password']=pswd
            messages.success(request, "Login successfully")
            return redirect(home_page)
        else:
            messages.warning(request, "Invalid Username or Password")
            return redirect(sign_in)
    else:
        messages.success(request, "Logout successfully")
        return redirect(sign_in)
def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(user_login)
def save_cart(request):
    if request.method=="POST":
        quantity=request.POST.get('quantity')
        total=request.POST.get('total')
        product_name=request.POST.get('Productname')
        username = request.POST.get('Username')
        price=request.POST.get('Price')
        try:
            x=productDB.objects.get(Product_name=product_name)
            img=x.Product_image
        except productDB.DoesNotExist:
            img=None
        obj=cartDB(Username=username,Product_name=product_name,Product_image=img,Price=price,Quantity=quantity,Total_price=total)
        obj.save()
        messages.success(request, "Cart saved")
        return redirect(home_page)
def cart_page(request):
    username = request.session.get('Username')  # Get Username safely
    if not username:
        return redirect('login_page')

    categories=categoryDB.objects.all()
    cart_count = cartDB.objects.filter(Username=username)
    x = cart_count.count()
    sub_total=0
    total_amount=0
    data = cartDB.objects.filter(Username=username)
    for i in data:
        sub_total +=i.Total_price
        if sub_total>300:
            shipping_amount=30
        else:
            shipping_amount=60
        total_amount=sub_total+shipping_amount
    return render(request,"cart.html",{'categories':categories,"data":data,"shipping_amount":shipping_amount,"sub_total":sub_total,"total_amount":total_amount,'x':x})
def checkout_page(request):
    username = request.session.get('Username')  # Get Username safely
    if not username:
        return redirect('login_page')

    categories = categoryDB.objects.all()
    cart_count = cartDB.objects.filter(Username=username)
    x = cart_count.count()
    sub_total = 0
    total_amount = 0
    data = cartDB.objects.filter(Username=username)
    for i in data:
        sub_total += i.Total_price
        if sub_total > 300:
            shipping_amount = 30
        else:
            shipping_amount = 60
        total_amount = sub_total + shipping_amount
    return render(request, "checkout.html", {'categories': categories,"data":data,"shipping_amount":shipping_amount,"sub_total":sub_total,"total_amount":total_amount,"x":x})
def save_checkout(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        message = request.POST.get('message')
        place = request.POST.get('place')
        pincode = request.POST.get('pincode')
        amount = request.POST.get('amount')
        obj = checkoutDB(Name=name, Email=email, Phone=phone, Address=address, Message=message, Place=place,
                         Pincode=pincode, Amount=amount)
        obj.save()
        return redirect(checkout_page)
def payment_page(request):
    username = request.session.get('Username')  # Get Username safely
    if not username:
        return redirect('login_page')

    # razorpay
    customer = checkoutDB.objects.order_by('-id').first()

    cart_count = cartDB.objects.filter(Username=username)
    x = cart_count.count()
    categories = categoryDB.objects.all()
    sub_total = 0
    total_amount = 0
    data = cartDB.objects.filter(Username=username)
    for i in data:
        sub_total += i.Total_price
        if sub_total > 300:
            shipping_amount = 30
        else:
            shipping_amount = 60
        total_amount = sub_total + shipping_amount

    # razorpay
    amount = int(total_amount * 100)
    pay_str = str(amount)
    if request.method == "POST":
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_yqWJ0dcaHSFLZP', 'JAbldBszWmbIf3RhnuBC79DU'))
        payment = client.order.create({'amount': amount, 'currency': order_currency})
    return render(request, "payment.html",
                  {'categories': categories, "data": data, "shipping_amount": shipping_amount, "sub_total": sub_total,
                   "total_amount": total_amount, "x": x,'customer':customer,'pay_str':pay_str})
def delete_cart(request,cart_id):
    p=cartDB.objects.filter(id=cart_id)
    p.delete()
    return redirect(cart_page)


@api_view(["GET"])
def product_recommendations_api(request, item_id):
    recommendations = get_recommended_products(item_id, limit=4)
    serializer = ProductRecommendationSerializer(
        recommendations,
        many=True,
        context={"request": request},
    )
    interactions = (
        productViewEvent.objects.values("product_id")
        .annotate(total_views=Count("id"))
        .order_by("-total_views")
    )
    return Response(
        {
            "product_id": item_id,
            "algorithm": "item-based collaborative filtering",
            "source": "customers also viewed",
            "recommendations": serializer.data,
            "interaction_count": productViewEvent.objects.count(),
            "top_viewed_product_ids": [row["product_id"] for row in interactions[:5]],
        }
    )
