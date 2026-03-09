from .models import Category, Order, OrderItem
from .forms import SignUpForm, LoginForm

def get_categories(request):
    categories = Category.objects.all()
    return {'categories':categories}

def cart_details(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        products_in_cart = OrderItem.objects.filter(order=order)
        cart_product_count = products_in_cart.count()

        return {'order':order, 'cart_products': products_in_cart, 'cart_product_count':cart_product_count,} 
    else:
        return {}
    
def get_forms(request):
    login_form = LoginForm()
    signup_form = SignUpForm()
    return {'login_form':login_form, 'signup_form':signup_form}