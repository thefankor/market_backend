from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import AddProdForm
from .models import Product, Category, Shop, Cart
from django.db.models import Avg, Count, Q, Sum, Min


# Create your views here.


def index(request):
    # products = Product.objects.filter(is_published=1)
    if request.user.is_authenticated and request.user.is_buyer:
        products = Product.objects.annotate(mark=Avg('reviews__score')).order_by('id').select_related('shop').annotate(
            count_in_cart=Min('cart__count', filter=Q(cart__user=request.user.buyer)))

    else:
        products = Product.objects.annotate(mark=Avg('reviews__score')).order_by('id').select_related('shop')
    return render(request, 'chipi/index_with_score.html', context={"prod": products})


def catg(request, cat_id):
    return render(request, 'chipi/cats.html', context={'cat_id': cat_id, })


def show_product(request, product_id):
    # return HttpResponse(f"PRODUCT {product_id}")
    product = get_object_or_404(Product, pk=product_id)
    data = {
        'title': product.title,
        'product': product,
    }
    return render(request, 'chipi/product.html', context=data)


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category_id=category.pk)
    return render(request, 'chipi/index.html', context={"prod": products})


def show_shop(request, seller_id):
    shop = get_object_or_404(Shop, pk=seller_id)
    products = Product.objects.filter(shop_id=shop.pk)
    return render(request, 'chipi/shop.html', context={"prod": products, "shop": shop})

# @login_required

def addprod(request):
    user = request.user
    if not user.is_shop:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    if request.method == 'POST':
        form = AddProdForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Product.objects.create(**form.cleaned_data, shop=user.shop)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления хз')

    else:
        form = AddProdForm()
    return render(request, 'chipi/addprod.html', {'form': form})



def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # data = {
    #     'title': product.title,
    #     'product': product,
    # }

    user = request.user
    if not user.is_shop:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    if user.shop != product.shop:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    form = AddProdForm(instance=product)

    if request.method == 'POST':
        form = AddProdForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('product', kwargs={'product_id': product.id}))
    return render(request, 'chipi/edit_product.html', {'form': form,})


def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)
    carts = Cart.objects.filter(user=request.user.buyer, product=product)
    if not carts.exists():
        Cart.objects.create(user=request.user.buyer, product=product, count=1)
    else:
        cart = carts.first()
        cart.count += 1
        cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_delete(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_decr(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    if cart.count != 1:
        cart.count -= 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_decr_in_index(request, product_id):
    cart = Cart.objects.get(product_id=product_id, user=request.user.buyer)
    if cart.count != 0:
        cart.count -= 1
        cart.save()
    else:
        cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def show_cart(request):
    if request.user.is_buyer:
        carts = Cart.objects.filter(user=request.user.buyer).order_by('-time_created')
        total_count = sum(cart.count for cart in carts)
        total_sum = sum(cart.sum() for cart in carts)
        data = {
            'products': carts,
            'total_count': total_count,
            'total_sum': total_sum,
        }
        return render(request, 'chipi/cart.html', context=data)
    elif request.user.is_shop:
        return HttpResponseNotFound('<h1>Корзина не доступна в режиме магазина</h1>')
    else:
        return redirect('users:login')

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')