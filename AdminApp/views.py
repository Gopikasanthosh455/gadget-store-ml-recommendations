from django.shortcuts import render,redirect

from AdminApp.models import categoryDB, productDB, serviceDB
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

from WebApp.models import contactDB
from django.contrib import messages


# Create your views here.
def index_page(request):
    category_count = categoryDB.objects.count()
    product_count = productDB.objects.count()
    contact_count = contactDB.objects.count()
    service_count = serviceDB.objects.count()
    return render(request,"index.html",{"category_count":category_count,"product_count":product_count,"contact_count":contact_count,"service_count":service_count})
def Add_category(request):
    return render(request,"Add_category.html")
def save_category(request):
    if request.method=="POST":
        category_name=request.POST.get('category')
        Description=request.POST.get('description')
        img=request.FILES['cat_profile']
        obj=categoryDB(Category_Name=category_name,Description=Description,cat_profile=img)
        obj.save()
        messages.success(request,"Category saved successfully")
        return redirect(Add_category)
def display_category(request):
    data=categoryDB.objects.all()
    return render(request,"Display_category.html",{"data":data})
def edit_category(request,cat_id):
    data=categoryDB.objects.get(id=cat_id)
    return render(request,"Edit_category.html",{"data":data})
def update_category(request,data_id):
    if request.method=="POST":
        cat_category_name=request.POST.get('category')
        cat_description=request.POST.get('description')
        try:
            h=request.FILES['cat_profile']
            fs=FileSystemStorage()
            file=fs.save(h.name, h)
        except MultiValueDictKeyError:
            file=categoryDB.objects.get(id=data_id).cat_profile
        categoryDB.objects.filter(id=data_id).update(Category_Name=cat_category_name,Description=cat_description,cat_profile=file)
        messages.success(request, "Category updated successfully")
        return redirect(display_category)
def delete_category(request,cat_id):
    T=categoryDB.objects.filter(id=cat_id)
    T.delete()
    messages.success(request, "Category deleted")
    return redirect(display_category)
def Add_product(request):
    data=categoryDB.objects.all()
    return render(request,"Add_product.html",{"data":data})
def save_product(request):
    if request.method=="POST":
        category_name=request.POST.get('category')
        description=request.POST.get('description')
        product_name=request.POST.get('product')
        price=request.POST.get('price')
        img=request.FILES['product_profile']
        obj=productDB(Category_name=category_name,Description=description,Product_image=img,Price=price,Product_name=product_name)
        obj.save()
        messages.success(request, "Product saved successfully")
        return redirect(Add_product)
def display_product(request):
    data=productDB.objects.all()
    return render(request,"display_product.html",{"data":data})
def delete_product(request,pro_id):
    p=productDB.objects.filter(id=pro_id)
    p.delete()
    messages.success(request, "Product deleted")
    return redirect(display_product)
def edit_product(request,pro_id):
    cat=categoryDB.objects.all()
    pro=productDB.objects.get(id=pro_id)
    return render(request,"Edit_product.html",{"pro":pro,"cat":cat})
def update_product(request,data_id):
    if request.method=="POST":
        pro_category_name=request.POST.get('category')
        pro_description=request.POST.get('description')
        pro_product_name=request.POST.get('product')
        pro_price=request.POST.get('price')
        try:
            h=request.FILES['product_profile']
            fs=FileSystemStorage()
            file=fs.save(h.name, h)
        except MultiValueDictKeyError:
            file=productDB.objects.get(id=data_id).Product_image
        productDB.objects.filter(id=data_id).update(Category_name=pro_category_name,Product_name=pro_product_name,Description=pro_description,Price=pro_price,Product_image=file)
        messages.success(request, "Product updated successfully")
        return redirect(display_product)
def admin_login(request):
    return render(request,"Admin_login.html")
def save_login(request):
    if request.method=="POST":
        un=request.POST.get('username')
        pswd=request.POST.get('pass')
        if User.objects.filter(username__contains=un).exists():
            x=authenticate(username=un,password=pswd)
            if x is not None:
                request.session['username']=un
                request.session['password']=pswd
                login(request,x)
                return redirect(index_page)
            else:
                return redirect(admin_login)
        else:
            return redirect(admin_login)
def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_login)
def contact_data(request):
    data=contactDB.objects.all()
    return render(request,"contact_data.html",{'data':data})
def delete_contact(request,con_id):
    contact=contactDB.objects.filter(id=con_id)
    contact.delete()
    messages.success(request, "contact deleted")
    return redirect(contact_data)
def AddService(request):
    return render(request,"AddServices.html")
def save_service(request):
    if request.method=="POST":
        service_name=request.POST.get('service')
        Description=request.POST.get('description')
        img=request.FILES['ser_profile']
        obj=serviceDB(service_Name=service_name,Description=Description,ser_profile=img)
        obj.save()
        messages.success(request, "Service saved successfully")
        return redirect(AddService)
def display_service(request):
    data=serviceDB.objects.all()
    return render(request,"Display_service.html",{"data":data})
def edit_service(request,ser_id):
    data=serviceDB.objects.get(id=ser_id)
    return render(request,"Edit_service.html",{"data":data})
def update_service(request,data_id):
    if request.method=="POST":
        ser_service_name=request.POST.get('service')
        ser_description=request.POST.get('description')
        try:
            h=request.FILES['ser_profile']
            fs=FileSystemStorage()
            file=fs.save(h.name, h)
        except MultiValueDictKeyError:
            file=serviceDB.objects.get(id=data_id).ser_profile
        serviceDB.objects.filter(id=data_id).update(service_Name=ser_service_name,Description=ser_description,ser_profile=file)
        messages.success(request, "Service updated successfully")
        return redirect(display_service)
def delete_service(request,ser_id):
    T=serviceDB.objects.filter(id=ser_id)
    T.delete()
    messages.success(request, "Service deleted")
    return redirect(display_service)

