from django import forms
from store.models import *
from account.models import *


class CustomerAddressRegister(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ("customer", "address", "city", "zip_code")


class OrderRegister(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["shipping_address"]


class OrderApproveStatus(forms.ModelForm):
    class Meta:
        model = OrderApprove
        fields = ["approve_status"]
