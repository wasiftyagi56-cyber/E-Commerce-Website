from django.shortcuts import render, redirect
# from .models import Product, Category, Customer, Order, OrderItem, ShippingAddress
from .models import *
from .forms import SignUpForm, LoginForm, QuantityForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    context = {'products':products,}
    
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
        return render(request, 'shop/cart.html')
    else:
        messages.info(request, "You need to log in first.")
        return redirect ("/")
    
def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)

        if request.method == "POST":
            # Take out the values (Shipping address) from the form 
            entered_address = request.POST['address']
            entered_city = request.POST['city']
            entered_state = request.POST['state']
            entered_zipcode = request.POST['zipcode']
            entered_country = request.POST['country']

            # Create a new Shipping Address Object 
            new_shipping_address = ShippingAddress.objects.create(customer=request.user.customer, order=order, address=entered_address, city=entered_city, state=entered_state, zipcode=entered_zipcode, country=entered_country)

            # Get the current order
            # Mark the order as completed
            order.completed = True
            order.total_price = order.totalCartPrice
            order.save()

            # Redirect to the home page
            messages.info(request, "Order Placed Successfully.")
            return redirect ("/")

        return render(request, 'shop/checkout.html')
    else:
        messages.info(request, "You need to log in first.")
        return redirect ("/")
    

def user_logout(request):
    logout(request)
    messages.info(
        request, "Logged out Successfully. Please log in to continue Shopping.")
    return redirect("/")
# Context Processors: 