import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.forms import modelformset_factory

from users.forms import AddressForm, PaymentTestForm
from users.models import Address
from .forms import AddProdForm, ImageForm
from .models import Product, Category, Shop, Cart, Favorite, Order, ProductImage
from django.db.models import Avg, Count, Q, Sum, Min


# Create your views here.


def index(request):
    # products = Product.objects.filter(is_published=1)
    if request.user.is_authenticated and request.user.is_buyer:
        carts = Cart.objects.filter(user=request.user.buyer).order_by('-time_created')
        for cart in carts:
            if cart.product.count == 0:
                cart.delete()
            elif cart.count > cart.product.count:
                cart.count = cart.product.count
                cart.save()

        fav_prod = Product.objects.filter(favorite__user=request.user.buyer)
        products = Product.objects.annotate(mark=Avg('reviews__score')).order_by('id').select_related('shop').annotate(
            count_in_cart=Min('cart__count', filter=Q(cart__user=request.user.buyer)))

    else:
        fav_prod = []
        products = Product.objects.annotate(mark=Avg('reviews__score')).order_by('id').select_related('shop')
    # return render(request, 'chipi/index_with_score.html', context={"prod": products, "fav_prod": fav_prod})
    return render(request, 'chipi/index2.html', context={"prod": products, "fav_prod": fav_prod})


def catg(request, cat_id):
    return render(request, 'chipi/cats.html', context={'cat_id': cat_id, })


def show_product(request, product_id):
    # return HttpResponse(f"PRODUCT {product_id}")
    product = get_object_or_404(Product, pk=product_id)
    photos = ProductImage.objects.filter(product=product)
    data = {
        'title': product.title,
        'product': product,
        'photos': photos,
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




def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)
    carts = Cart.objects.filter(user=request.user.buyer, product=product)
    if not carts.exists():
        Cart.objects.create(user=request.user.buyer, product=product, count=1)
    else:
        cart = carts.first()
        if int(product.count) > int(cart.count):
            cart.count += 1
        cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_add_ajax(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)
    carts = Cart.objects.filter(user=request.user.buyer, product=product)
    if not carts.exists():
        Cart.objects.create(user=request.user.buyer, product=product, count=1)
        if int(product.count) <= 2:
            response_data = {'status': 'success', 'product_id': product.id, 'last': True, 'max': True}
        else:
            response_data = {'status': 'success', 'product_id': product.id, 'last': False, 'max': True}
    else:
        cart = carts.first()
        if int(product.count) <= int(cart.count) + 1:
            response_data = {'status': 'success', 'product_id': product.id, 'last': True, 'max': True}
        else:
            response_data = {'status': 'success', 'product_id': product.id, 'last': False, 'max': True}
        if int(product.count) > int(cart.count):
            cart.count += 1
            response_data['max'] = False

        cart.save()

    # response_data = {'status': 'success', 'product_id': product.id, 'aaa': 'bbb'}
    return JsonResponse(response_data)
    # return render('home')

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
    if cart.count != 1:
        cart.count -= 1
        cart.save()
    else:
        cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_decr_in_index_ajax(request):
    product_id = request.POST.get("product_id")
    cart = Cart.objects.get(product_id=product_id, user=request.user.buyer)
    if cart.count != 1:
        cart.count -= 1
        cart.save()
    else:
        cart.delete()
    response_data = {'status': 'success', 'aaa': 'bbb'}
    return JsonResponse(response_data)


def show_cart(request):
    try:
        if request.user.is_buyer:
            carts = Cart.objects.filter(user=request.user.buyer).order_by('-time_created')
            new_cart = []
            for cart in carts:
                if cart.product.count == 0:
                    cart.delete()
                elif cart.count > cart.product.count:
                    cart.count = cart.product.count
                    cart.save()
                    new_cart.append(cart)
                else:
                    new_cart.append(cart)

            carts = new_cart
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
    except:
        return redirect('users:login')


def create_order(request):
    try:
        if request.user.is_buyer:
            user = request.user
            indata = {
                'phone': user.buyer.phone,
                'email': user.buyer.email,
                'last_name': user.buyer.last_name,
                'first_name': user.buyer.first_name,
                'middle_name': user.buyer.middle_name,
            }
            if user.buyer.correct_address:
                form = AddressForm(instance=user.buyer.correct_address)
            else:
                form = AddressForm(initial=indata)
            if request.method == 'POST':
                form = AddressForm(request.POST)
                if form.is_valid():
                    try:
                        if not user.buyer.correct_address:
                            a = Address.objects.create(**form.cleaned_data, user=user.buyer)
                            u = user.buyer
                            u.correct_address = a
                            u.save()
                        else:
                            adr = user.buyer.correct_address.id
                            Address.objects.filter(pk=adr).update(**form.cleaned_data)
                        return redirect('create_order')
                    except:
                        form.add_error(None, 'Ошибка добавления хз')
                    # return redirect(reverse_lazy('order'))

            carts = Cart.objects.filter(user=request.user.buyer).order_by('-time_created')
            if len(carts) == 0:
                return redirect('home')
            else:
                total_count = sum(cart.count for cart in carts)
                total_sum = sum(cart.sum() for cart in carts)
                data = {
                    'products': carts,
                    'total_count': total_count,
                    'total_sum': total_sum,
                    'form': form,
                }
                return render(request, 'chipi/create_order.html', context=data)
        elif request.user.is_shop:
            return HttpResponseNotFound('<h1>Оформление заказа недоступно в режиме магазина</h1>')
        else:
            return redirect('users:login')
    except:
        return redirect('users:login')


def pay_order(request):
    # try:
    if request.user.is_buyer:
        user = request.user
        carts = Cart.objects.filter(user=request.user.buyer).order_by('-time_created')
        address = user.buyer.correct_address
        if not user.buyer.correct_address:
            return redirect('users:address')
        form = PaymentTestForm()
        if request.method == 'POST':
            form = PaymentTestForm(request.POST)
            if form.is_valid():
                try:
                    for c in carts:
                        if c.count > c.product.count:
                            form.add_error(None, 'Количество доступных товаров изменилось')
                            return redirect(reverse_lazy('pay_order'))
                    for cart in carts:
                        cart.product.count = cart.product.count - cart.count
                        cart.product.save()
                        Order.objects.create(user=user.buyer, product=cart.product, shop=cart.product.shop,
                                             count=cart.count,
                                             price=cart.product.price,
                                             title=cart.product.title,
                                             first_name=address.first_name,
                                             middle_name=address.middle_name,
                                             last_name=address.last_name,
                                             email=address.email,
                                             phone=address.phone,
                                             country=address.country,
                                             region=address.region,
                                             city=address.city,
                                             index=address.index,
                                             addr=address.addr)
                        cart.delete()

                    return redirect('orders')
                except:
                    form.add_error(None, 'Ошибка оплаты хз')
                # return redirect(reverse_lazy('order'))


        if len(carts) == 0:
            return redirect('home')
        else:
            total_count = sum(cart.count for cart in carts)
            total_sum = sum(cart.sum() for cart in carts)
            data = {
                'total_count': total_count,
                'total_sum': total_sum,
                'form': form,
            }
            return render(request, 'chipi/pay_order.html', context=data)
    elif request.user.is_shop:
        return HttpResponseNotFound('<h1>Оформление заказа недоступно в режиме магазина</h1>')
    else:
        return redirect('users:login')
    # except:
    #     return redirect('users:login')


def add_fav(request, product_id):
    product = Product.objects.get(id=product_id)
    if len(Favorite.objects.filter(user=request.user.buyer, product_id=product_id)) == 0:
        Favorite.objects.create(user=request.user.buyer, product=product)
    # request.user.buyer.favorite.add(product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def rem_fav(request, product_id):

    fav = Favorite.objects.get(user=request.user.buyer, product=product_id)

    fav.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_favorites(request):
    if request.user.is_buyer:
        favs = Product.objects.filter(favorite__user=request.user.buyer).annotate(
            mark=Avg('reviews__score')).order_by('id').select_related('shop').annotate(
            count_in_cart=Min('cart__count', filter=Q(cart__user=request.user.buyer)))
        return render(request, 'chipi/favorites.html', context={"prod": favs})
    elif request.user.is_shop:
        return HttpResponseNotFound('<h1>Список желаний не доступен в режиме магазина</h1>')
    else:
        return redirect('users:login')


def show_orders(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse_lazy('users:login'))
    if not user.is_buyer:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')


    orders = Order.objects.filter(user=request.user.buyer).order_by('-time_created')

    return render(request, 'chipi/orders.html', context={"orders":orders})


def show_orders_for_shop(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse_lazy('users:login'))
    if not user.is_shop:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    orders = Order.objects.filter(shop=request.user.shop).order_by('-time_created')

    return render(request, 'chipi/orders_shop.html', context={"orders":orders})


def addprod(request):
    user = request.user

    if not user.is_shop:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    if request.method == 'POST':
        form = AddProdForm(request.POST, request.FILES)


        if form.is_valid():
            # print(form.cleaned_data)
            try:
                prod = Product.objects.create(**form.cleaned_data, shop=user.shop)
                files = request.FILES.getlist('files')

                for f in files:
                    a = ProductImage(product=prod, image=f)
                    a.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления хз')

    else:
        form = AddProdForm()

    return render(request, 'chipi/addprod.html', {'form': form,})



def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    photos = ProductImage.objects.filter(product=product)

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
        form = AddProdForm(request.POST, request.FILES, instance=product)
        if form.is_valid():

            form.save()
            files = request.FILES.getlist('files')
            if len(files) > 0:
                prim = ProductImage.objects.filter(product=product)
                for pr in prim:
                    if os.path.isfile(pr.image.path):
                        os.remove(pr.image.path)
                    pr.delete()
            for f in files:
                a = ProductImage(product=product, image=f)
                a.save()
            return redirect(reverse_lazy('edit_product', kwargs={'product_id': product.id}))
    return render(request, 'chipi/edit_product.html', {'form': form, 'product': product,
                                                       'photos': photos})