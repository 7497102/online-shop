from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Product, Category
from random import randint

from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *


# Create your views here.


# class ProductList(ListView):
#     model = Product
#     context_object_name = 'categories'
#     # products = Product.objects.all()
#     # context = {
#     #     'products': products
#     # }
#     extra_context = {
#         'title': 'TOTEMBO: Главная страница'
#     }
#     # context = {
#     #     'title': 'TOTEMBO: Главная страница',
#     #     'products': products
#     # }
#     template_name = 'store/product_list.html'
#
#     def get_queryset(self):
#         categories = Category.objects.filter(parent=None)
#         return categories

def product_list(request):
    return render(request, 'store/product_list.html')


# class CategoryView(ListView):
#     model = Product
#     context_object_name = 'products'
#     template_name = 'store/category_page.html'
#
#     def get_queryset(self):
#         main_category = Category.objects.get(slug=self.kwargs['slug'])
#         subcategories = main_category.subcategories.all()
#         data = []
#         for subcategory in subcategories:
#             products = subcategory.products.all()
#             for product in products:
#                 data.append(product)
#         return data

def category_page(request, slug):
    main_category = Category.objects.get(slug=slug)
    subcategories = main_category.subcategories.all()
    products = Product.objects.filter(category__in=subcategories)
    colors = []
    materials = []
    for product in products:
        colors.append(product.color)
        materials.append(product.material)
    context = {
        'products': products,
        'main_category': main_category,
        'colors': colors,
        'materials': materials
    }
    sort_fields = request.GET.get('sort')
    if sort_fields:
        context['products'] = products.order_by(sort_fields)
    type_fields = request.GET.get('type')
    if type_fields:
        context['products'] = Product.objects.filter(category__slug=type_fields)
    color_fields = request.GET.get('color')
    if color_fields:
        context['products'] = Product.objects.filter(color=color_fields)
    material_fields = request.GET.get('material')
    if material_fields:
        context['products'] = Product.objects.filter(material=material_fields)

    return render(request, 'store/category_page.html', context)


# class ProductDetail(DetailView):
#     model = Product
#     context_object_name = 'product'


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    products = Product.objects.all()  # 20
    data = []

    for i in range(4):
        #
        random_index = randint(0, len(products) - 1)
        p = products[random_index]
        if p not in data:
            data.append(p)

    context = {
        'title': f'Товар: {product.title}',
        'product': product,
        'products': data,
        'reviews': Review.objects.filter(product__slug=slug)
    }
    if request.user.is_authenticated:
        context['review_form'] = ReviewForm()

    return render(request, 'store/product_detail.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Sign out successfully !')
    return redirect('product_list')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Sign in successfully !')
                return redirect('product_list')
            else:
                messages.error(request, 'Username or password is incorrect !')
                return redirect('login')
        else:
            messages.error(request, 'Username or password is incorrect !')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'title': 'Sign in',
        'form': form
    }

    return render(request, 'store/user_login.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sign up successfully !')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'title': 'Sign up',
        'form': form
    }

    return render(request, 'store/register.html', context)



def save_review(request, product_id):
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        review.product_id = product_id
        review.save()
    else:
        pass
    product = Product.objects.get(pk=product_id)
    return redirect('product_detail', product.slug)



def cart(request):
    return render(request, 'store/cart.html')


def to_cart(request, product_id, action):
    return redirect('cart')


def checkout(request):
    context = {
        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm(),
        'title': 'Checkout'
    }