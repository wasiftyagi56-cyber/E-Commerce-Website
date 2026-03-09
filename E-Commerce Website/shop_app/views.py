from django.shortcuts import render, redirect
from .models import Product, Category, Customer, Order, OrderItem
from .forms import SignUpForm, LoginForm, QuantityForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    form = SignUpForm()
    products = Product.objects.all()
    context = {'products':products, 'form':form,}
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        products_in_cart = OrderItem.objects.filter(order=order)
        cart_product_count = products_in_cart.count()
        context = {'products':products, 'form':form, 'order':order, 'cart_products': products_in_cart, 'cart_product_count':cart_product_count}
    
    return render(request, 'shop/index.html', context)

def add_to_cart(request, id):
    if request.method == "POST":
        form = QuantityForm(request.POST)
        if form.is_valid():
            product_quantity = form.cleaned_data['quantity']
            
            product = Product.objects.get(id=id)

            order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)

            total_price = product.price * product_quantity

            added_item = OrderItem(order=order, product=product, quantity=product_quantity, total_price=total_price)
            added_item.save()

            messages.info(request, "Product Added Successfully")
            return redirect('/shop')
        
        else:
            messages.info(request, "Something went wrong, please try again.")
            return redirect('/shop')
        
        # redirect back to the last page 
    return redirect ('/shop')

def all_products(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products':products})

def single_product(request, name):
    quantity_form = QuantityForm()
    
    product = Product.objects.get(name=name)
    return render (request, 'shop/single_product.html', {'product':product, 'form':quantity_form})

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            conf_password = form.cleaned_data['conf_password']
            phone = form.cleaned_data['phone']

            if password == conf_password:
                if User.objects.filter(username=username).exists():

                    # Message: User name already exists
                    messages.info(
                        request, "Username already exists. Please try again")

                    # Redirect to the signup page
                    return redirect("/")
                else:
                    # New User create
                    new_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)

                    # New Customer Create
                    Customer.objects.create(user=new_user, phone=phone, email=email, full_name=first_name+" "+last_name)

                    # Redirect to the login page
                    messages.info(request, "Signup successful. Please login now")
                    return redirect("/")
            else:
                # Message: Passwords do not match
                messages.info(request, "Passwords do not match. Please try again.")

                # Redirect to the signup page
                return redirect("/")

    return redirect("/")

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                # login the user
                messages.info(request, "Logged in Successfully. Enjoy your shopping now")
                login(request, user)
                return redirect("/")
                # else:
            else:
                # Message: Invalid credentials. Please try again.
                messages.info(request, "Invalid credentials. Please try again")
                # redirect to the login page
                return redirect("/")

    return redirect("/")


def cart_details(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        products_in_cart = OrderItem.objects.filter(order=order)
        cart_product_count = products_in_cart.count()
        context = {'cart_products': products_in_cart, 'order':order, 'cart_product_count':cart_product_count,}
        return render(request, 'shop/cart.html', context)
    else:
        messages.info("You need to log in first.")
        return redirect ("/")
    
def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        products_in_cart = OrderItem.objects.filter(order=order)
        cart_product_count = products_in_cart.count()
        context = {'cart_products': products_in_cart, 'order':order, 'cart_product_count':cart_product_count,}
        return render(request, 'shop/checkout.html', context)
    else:
        messages.info("You need to log in first.")
        return redirect ("/")
    
# Context Processors: 