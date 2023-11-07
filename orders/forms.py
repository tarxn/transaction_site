from django import forms
from .models import books_map

class AddOrderForm(forms.Form):
    BOOK_CHOICES = [('book-1', 'Book 1'), ('book-2', 'Book 2'), ('book-3', 'Book 3')]
    OPERATION_CHOICES = [('BUY', 'Buy'), ('SELL', 'Sell')]

    book = forms.ChoiceField(choices=BOOK_CHOICES, label='Book', required=True)
    operation = forms.ChoiceField(choices=OPERATION_CHOICES, label='Operation', required=True)
    price = forms.FloatField(label='Price', min_value=0, required=True)
    volume = forms.IntegerField(label='Volume', min_value=1, required=True)
    order_id = forms.IntegerField(label='Order ID', min_value=1, required=True)

class DeleteOrderForm(forms.Form):
    order_id = forms.IntegerField(label='Order ID', min_value=1, required=True)
    book = forms.ChoiceField(choices=[(book_name, book_name) for book_name in books_map.keys()])
