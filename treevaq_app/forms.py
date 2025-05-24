# dsi202/my_django_project/treevaq_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, CartItem # Import CartItem model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # เพิ่ม email field เข้ามาด้วย

class AddToCartForm(forms.Form):
    # This form could be used if you want to allow users to specify quantity
    # right when adding to cart from a product detail page.
    # For now, we'll assume a simple "add 1" from product list.
    # If you need a quantity input on product pages, uncomment and use this.
    # quantity = forms.IntegerField(min_value=1, initial=1)
    pass

class UpdateCartQuantityForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 99}),
        }