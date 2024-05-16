from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.db import transaction

from chipi.models import Shop
from users.models import Buyer, Address


# from .models import Product, Category, Shop


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'account-p-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'parol-password', 'id': 'password'}))
    # is_buyer = forms.BooleanField(initial=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    # def confirm_login_allowed(self, model):
    #     if not model.is_buyer:
    #         raise ValidationError(("This account isnt buyer."))



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'account-p-input',}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'parol-password', 'id': 'password-1'}))
    password2 = forms.CharField(label='Password again', widget=forms.PasswordInput(attrs={'class': 'parol-password', 'id': 'password-2'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'account-p-input',}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'account-p-input', }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'phone', 'email']
        labels = {
            'email': 'E-mail',
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_buyer = True
        user.save()
        buyer = Buyer.objects.create(user=user)
        buyer.phone = self.cleaned_data['phone']
        buyer.email = self.cleaned_data['email']
        buyer.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует!')
        return email


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # if get_user_model().objects.filter(email=email).exists():
        if ((len(phone) != 12 and phone[0] != '8') or (len(phone) != 11 and phone[:2] != '+7')):
            raise forms.ValidationError('Введите кореектный RU номер телефона в формате +79995554433!')
        if phone[0] == '8':
            phone_new = '7'+phone[1:]
        else:
            phone_new = phone[1:]
        if get_user_model().objects.filter(buyer__phone=phone_new).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует!')
        if get_user_model().objects.filter(shop__phone=phone_new).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует!')
        return phone_new


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'settings-left-1-input',}))
    # email = forms.CharField(disabled=True, label='Email', widget=forms.TextInput())
    # buyer__id = forms.IntegerField(disabled=True)
    # buyer__phone = forms.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ['username',]
        # labels = {
        #     'email': 'E-mail',
        # }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует!')
        return email

class ProfileUser2Form(forms.ModelForm):
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'settings-left-1-input',}))
    email = forms.CharField(label='EMail', widget=forms.TextInput(attrs={'class': 'settings-right-1-input', }))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'settings-right-1-input', }))
    first_name = forms.CharField(label='first Name', widget=forms.TextInput(attrs={'class': 'settings-left-1-input', }))
    middle_name = forms.CharField(label='Middle Name', widget=forms.TextInput(attrs={'class': 'settings-right-1-input', }))

    # user = forms.IntegerField(disabled=True)
    class Meta:
        model = Buyer
        fields = ['phone', 'email', 'last_name', 'first_name', 'middle_name']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'phone': 'Номер телефона',
        }
    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if 0<len(name)<2:
            raise forms.ValidationError('Имя должно состоять минимум из двух букв')
        for sym in name.lower():
            if sym not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                raise forms.ValidationError('Имя может содержать только латинские или русские буквы!')
        return name

    def clean_middle_name(self):
        name = self.cleaned_data['middle_name']
        if 0<len(name)<2:
            raise forms.ValidationError('Отчество должно состоять минимум из двух букв')
        for sym in name.lower():
            if sym not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                raise forms.ValidationError('Отчество может содержать только латинские или русские буквы!')
        return name

    def clean_last_name(self):
        name = self.cleaned_data['last_name']
        if 0<len(name)<2:
            raise forms.ValidationError('Фамилия должна состоять минимум из двух букв')
        for sym in name.lower():
            if sym not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                raise forms.ValidationError('Фамилия может содержать только латинские или русские буквы!')
        return name


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password",widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="New password confirmation", widget=forms.PasswordInput())


class RegisterShopForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'account-p-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'parol-password', 'id': 'password-1'}))
    password2 = forms.CharField(label='Password again', widget=forms.PasswordInput(attrs={'class': 'parol-password', 'id': 'password-2'}))
    name = forms.CharField(label='Shop name', widget=forms.TextInput(attrs={'class': 'account-p-input'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'account-p-input'}))
    email = forms.EmailField(label='shop email', widget=forms.TextInput(attrs={'class': 'account-p-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']
        # labels = {
        #     'first_name': 'Имя',
        #     'last_name': 'Фамилия',
        # }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_shop = True
        user.save()
        shop = Shop.objects.create(user=user)
        shop.name = self.cleaned_data['name']
        shop.phone = self.cleaned_data['phone']
        shop.email = self.cleaned_data['email']
        shop.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(shop__email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует!')
        if get_user_model().objects.filter(buyer__email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует!')
        return email


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # if get_user_model().objects.filter(email=email).exists():
        if ((len(phone) != 12 and phone[0] != '8') or (len(phone) != 11 and phone[:2] != '+7')):
            raise forms.ValidationError('Введите кореектный RU номер телефона в формате +79995554433!')
        if phone[0] == '8':
            phone_new = '7' + phone[1:]
        else:
            phone_new = phone[1:]
        if get_user_model().objects.filter(buyer__phone=phone_new).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует!')
        if get_user_model().objects.filter(shop__phone=phone_new).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует!')
        return phone_new


class ProfileShopForm(forms.ModelForm):
    #
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'settings-left-1-input',}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'settings-left-1-input', }))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'settings-left-1-input', }))
    # id = forms.IntegerField(disabled=True)
    class Meta:
        model = Shop
        fields = ['phone', 'email', 'name']
        labels = {
            'email': 'E-mail',
            'phone': 'Номер телефона',
            'name': 'Название магазина',
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # if get_user_model().objects.filter(email=email).exists():
        if (( len(phone) != 12 and phone[0] != '8' and phone[0] != '7' ) or (len(phone) != 11 and phone[:2] != '+7')):
            raise forms.ValidationError('Введите кореектный RU номер телефона в формате +79995554433!')
        if phone[0] == '7':
            phone_new = phone
        elif phone[0] == '8':
            phone_new = '7' + phone[1:]
        else:
            phone_new = phone[1:]
        return phone_new


class AddressForm(forms.ModelForm):
    first_name = forms.CharField(label='first Name', widget=forms.TextInput(attrs={'class': 'adress-111-input first-name-input', }))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'adress-112-input last-name-input', }))
    middle_name = forms.CharField(label='Middle Name',
                                  widget=forms.TextInput(attrs={'class': 'adress-12-input middle-name-input', }))
    addr = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'adress-12-input adress-input', }))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'adress-12-input land-input', }))
    region = forms.CharField(label='Region', widget=forms.TextInput(attrs={'class': 'adress-12-input region-input', }))
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'adress-111-input city-input', }))
    index = forms.CharField(label='Index', widget=forms.TextInput(attrs={'class': 'adress-112-input index-input', }))
    # adress-111-input
    # id = forms.IntegerField()
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'adress-12-input phone-input', }))
    email = forms.CharField(label='EMail', widget=forms.TextInput(attrs={'class': 'adress-12-input email-input', }))

    # phone = forms.CharField()

    class Meta:
        model = Address
        fields = ['phone', 'email', 'last_name', 'first_name', 'middle_name', 'country', 'region', 'city', 'index', 'addr']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # if get_user_model().objects.filter(email=email).exists():
        if (( len(phone) != 12 and phone[0] != '8' and phone[0] != '7' ) or (len(phone) != 11 and phone[:2] != '+7')):
            raise forms.ValidationError('Введите кореектный RU номер телефона в формате +79995554433!')
        if phone[0] == '7':
            phone_new = phone
        elif phone[0] == '8':
            phone_new = '7' + phone[1:]
        else:
            phone_new = phone[1:]
        return phone_new

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if 0<len(name)<2:
            raise forms.ValidationError('Имя должно состоять минимум из двух букв')
        for sym in name.lower():
            if sym not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                raise forms.ValidationError('Имя может содержать только латинские или русские буквы!')
        return name

    def clean_middle_name(self):
        name = self.cleaned_data['middle_name']
        if 0<len(name)<2:
            raise forms.ValidationError('Отчество должно состоять минимум из двух букв')
        for sym in name.lower():
            if sym not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                raise forms.ValidationError('Отчество может содержать только латинские или русские буквы!')
        return name

    def clean_last_name(self):
        name = self.cleaned_data['last_name']
        if 0<len(name)<2:
            raise forms.ValidationError('Фамилия должна состоять минимум из двух букв')
        for sym in name.lower():
            if sym not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                raise forms.ValidationError('Фамилия может содержать только латинские или русские буквы!')
        return name


class PaymentTestForm(forms.Form):
    card_num = forms.CharField(widget=forms.TextInput(attrs={'class': 'nomer', 'placeholder': '1234 5678 9012 3456', 'id': 'cardNumber'}))
    card_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'data-input', 'placeholder': '12/24', 'id': 'cardData'}))
    card_cvv = forms.CharField(widget=forms.TextInput(attrs={'class': 'cvv-input', 'placeholder': '156', 'id': 'cardCvv'}))