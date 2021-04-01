from django.shortcuts import get_object_or_404, render
from .models import Category, Product


from django.shortcuts import render
from . import forms
from django.core.mail import send_mail
from django_project.settings import EMAIL_HOST_USER


def home(request):

    products = Product.products.all()

    return render(request,
                  'store/home.html',
                  {'products': products})


def notify(request):
    sub = forms.Notify()
    if request.method == 'POST':
        sub = forms.Notify(request.POST)
        subject = 'Welcome to telexi'
        message = 'telexi will be available June 1'
        recipient = str(sub['Email'].value())
        send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
        return render(request, 'store/notify/success.html', {'recipient': recipient})
    return render(request, 'store/notify/index.html', {'form': sub})


def categories(request):

    return {
        'categories': Category.objects.all()
    }


def product_all(request):

    products = Product.products.all()

    return render(request,
                  'store/products.html',
                  {'products': products})


def category_list(request, category_slug):

    category = get_object_or_404(Category,
                                 slug=category_slug)
    products = Product.objects.filter(category=category)

    return render(request,
                  'store/category.html',
                  {
                      'category': category,
                      'products': products
                  })


def product_detail(request, slug):

    product = get_object_or_404(Product,
                                slug=slug,
                                in_stock=True)
    return render(request,
                  'store/single.html',
                  {'product': product})
