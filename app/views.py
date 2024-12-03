from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout, login as auth_login

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    catcategories = Catcategory.objects.all()
    

    context = {
        'products': products,
        'categories': categories,
        'catcategories': catcategories,
    }
    return render(request, 'home.html', context)

def product_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def prod(request, id):
    products = Product.objects.filter(category__id=id)
    return render(request, 'prod.html', {'products': products})

def viewproduct(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()
    catcategories = Catcategory.objects.all()

    context = {
        'categories': categories,
        'catcategories': catcategories,
        'product': product,
    }
    return render(request, 'viewproduct.html', context)

def category_view(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})

def catcategory_products(request, id):
    catcategory = Catcategory.objects.get(id=id)
    products = Product.objects.filter(catcategory=catcategory)
   
    categories = Category.objects.all()

    catcategories = Catcategory.objects.all()
    

    context = {
        
        'categories': categories,
        'catcategories': catcategories,
        'catcategory': catcategory,
        'products': products
    }
    return render(request, 'productby_category.html', context)


def mens_wear(request):
    
    mens_wear_category = Category.objects.filter(name__in=["Men's Wear", "Men's Formal"])
    products = Product.objects.filter(category__in=mens_wear_category)
    
    return render(request, 'menswearnew.html', {'products': products})
def womens_wear(request):
    
    womens_wear_category = Category.objects.filter(name__in=['Women\'s Wear','Women Ethnic'])
    products=Product.objects.filter(category__in=womens_wear_category)
    
    return render(request, 'womeswear.html', {'products': products})
def westernwear(request):
    
    western_wear_category = Category.objects.filter(name__in=["Western Wear"])
    products = Product.objects.filter(category__in=western_wear_category)
    
    return render(request, 'westernwear.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        print(user)
        messages.success(request, 'Signup successful! You can now log in.')
        return redirect('loginpage')
    else:
        return redirect('home')
def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            if user.is_superuser:

                return redirect('home')
            else:
                return redirect('cartpage')
        else:
            messages.error(request,'invalid credential')
            return redirect('loginpage')
    return redirect('home')
def logoutpage(request):
    logout(request) 
    return redirect('home')  
def remove(request,id):
    if request.user.is_authenticated:
        cart_items=Cart.objects.get(id=id,user=request.user)
        cart_items.delete()
        return redirect('cartpage')
    else:
        return redirect('loginpage')
def wishlist(request,id):
    if request.user.is_authenticated:
        product=Product.objects.get(id=id)
        wishlist=Wishlist.objects.filter(user=request.user,product=product).first()
        if wishlist:
            return redirect('wishpage')
        else:
            wishlist=Wishlist.objects.create(user=request.user,product=product)
            wishlist.save()
            return redirect('wishpage')
    else:
        return redirect('loginpage') 
def wishpage(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        return render(request, 'wishlist.html',{'wishlist':wishlist})
    else:
        return redirect('loginpage' )
def removewish(request,id):
    if request.user.is_authenticated:
        wish_items=Wishlist.objects.get(id=id,user=request.user)
        wish_items.delete()
        return redirect('wishpage')
    else:
        return redirect('loginpage')
def place_order(request):
    cart_items=Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('home')
    exist_order=Order.objects.filter(user=request.user).first()
    if request.method=='POST':
        address=request.POST['address']
        if exist_order:
            exist_order.address=address
            exist_order.save()
        else:
            orders=Order.objects.create(user=request.user,address=address)
        cart_items.delete()
        return redirect('confirm')
    return render(request,'place_order.html',{'cart_items':cart_items,'user':request.user,'exist_address':exist_order.address if exist_order else ''})
def order_confirmation(request):
    return render(request,'order_confirmation.html')
from django.shortcuts import render
from .models import Product


def product_search(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        results = []  # No query, return an empty list
    
    return render(request, 'search.html', {'query': query, 'results': results})
def addcart(request, id):
    product = Product.objects.get(id=id)
    
    if request.user.is_authenticated:
        user = request.user
        cart_item = Cart.objects.filter(user=user, product=product).first()
        
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            Cart.objects.create(user=user, product=product, quantity=1)
        
        return redirect('cartpage')
    else:
        cart = request.session.get('cart', [])
        for item in cart:
            if item['product_id'] == id:
                item['quantity'] += 1
                break
        else:
            cart.append({'product_id': id, 'quantity': 1})
        
        request.session['cart'] = cart
        return redirect('loginpagecart')
def cartpage(request):
    if request.user.is_authenticated:
        user = request.user
        
        session_cart = request.session.get('cart', [])
        for item in session_cart:
            product = Product.objects.get(id=item['product_id'])
            cart_item = Cart.objects.filter(user=user, product=product).first()
            
            if cart_item:
                cart_item.quantity += item['quantity']
                cart_item.save()
            else:
                Cart.objects.create(user=user, product=product, quantity=item['quantity'])
        
        request.session['cart'] = []
        
        cart_items = Cart.objects.filter(user=user)
        totalprice = sum(i.quantity * i.product.rate for i in cart_items)
        
        both = {
            'products_in_cart': cart_items,
            'total': totalprice,
        }
        return render(request, 'cart.html', both)
    else:
        return redirect('loginpagecart')


def logincart(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            session_cart = request.session.get('cart', [])
            for item in session_cart:
                product = Product.objects.get(id=item['product_id'])
                cart_item = Cart.objects.filter(user=user, product=product).first()
                if cart_item:
                    cart_item.quantity += item['quantity']
                    cart_item.save()
                else:
                    Cart.objects.create(user=user, product=product, quantity=item['quantity'])
            
            request.session['cart'] = []
            
            return redirect('cartpage')  
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')


def signupcart(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        
        
        if User.objects.filter(username=username).exists():
            context = {'error': 'Username already exists'}
            return render(request, 'signup.html', context)
        
        if User.objects.filter(email=email).exists():
            context = {'error': 'Email already exists'}
            return render(request, 'signup.html', context)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        
        session_cart = request.session.get('cart', [])
        for item in session_cart:
            product = Product.objects.get(id=item['product_id'])
            cart_item = Cart.objects.filter(user=user, product=product).first()
            if cart_item:
                cart_item.quantity += item['quantity']
                cart_item.save()
            else:
                Cart.objects.create(user=user, product=product, quantity=item['quantity'])
        
        request.session['cart'] = []
        
        return redirect('cartpage')
    
    return render(request, 'signup.html')
def wishlist(request, id):
    product = Product.objects.get(id=id)
    
    if request.user.is_authenticated:
        user = request.user
        wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
        
        if not wishlist_item:
            Wishlist.objects.create(user=user, product=product)
        
        return redirect('wishpage')
    else:
        wishlist = request.session.get('wishlist', [])
        if id not in wishlist:
            wishlist.append(id)
        
        request.session['wishlist'] = wishlist
        return redirect('loginpagewish')
def wishpage(request):
    if request.user.is_authenticated:
        user = request.user
        
        session_wishlist = request.session.get('wishlist', [])
        for product_id in session_wishlist:
            product = Product.objects.get(id=product_id)
            wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
            
            if not wishlist_item:
                Wishlist.objects.create(user=user, product=product)
        
        request.session['wishlist'] = []
        
        wishlist_items = Wishlist.objects.filter(user=user)
        return render(request, 'wishlist.html', {'wishlist': wishlist_items})
    else:
        session_wishlist = request.session.get('wishlist', [])
        products = Product.objects.filter(id__in=session_wishlist)
        return render(request, 'wishlist.html', {'wishlist': products})
def loginwishlist(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            session_wishlist = request.session.get('wishlist', [])
            for product_id in session_wishlist:
                product = Product.objects.get(id=product_id)
                wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
                
                if not wishlist_item:
                    Wishlist.objects.create(user=user, product=product)
            
            
            request.session['wishlist'] = []
            
            return redirect('wishpage')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'loginwish.html', context)
    return render(request, 'loginwish.html')
def signupwishlist(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        
        if User.objects.filter(username=username).exists():
            context = {'error': 'Username already exists'}
            return render(request, 'signupwish.html', context)
        
        if User.objects.filter(email=email).exists():
            context = {'error': 'Email already exists'}
            return render(request, 'signupwish.html', context)
        
        
        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        
        
        session_wishlist = request.session.get('wishlist', [])
        for product_id in session_wishlist:
            product = Product.objects.get(id=product_id)
            wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
            
            if not wishlist_item:
                Wishlist.objects.create(user=user, product=product)
        
        
        request.session['wishlist'] = []
        
        return redirect('wishpage')
    
    return render(request, 'signupwish.html')
