from django.shortcuts import render
from django.http import HttpResponse
from .forms import AddOrderForm, DeleteOrderForm
from .models import Order, Book, books_map  # Assuming that you have converted the provided code into Django model form

# Function to format the book for HttpResponse
def format_book(book):
    response = f"Book: {book.name}\n"
    response += "Buy Orders:\n"
    for order in book.buy_orders:
        response += f"{order.volume}@{order.price}\n"
    response += "Sell Orders:\n"
    for order in book.sell_orders:
        response += f"{order.volume}@{order.price}\n"
    return response

def add_order(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        print("reached ckp1")
        if form.is_valid():
            book_name = form.cleaned_data['book']
            order_ = Order(
                book=book_name,
                operation=form.cleaned_data['operation'],
                price=form.cleaned_data['price'],
                volume=form.cleaned_data['volume'],
                order_id=form.cleaned_data['order_id']
            )
            print("reached ckp2")
            books_map[book_name].add_order(order_)
            book_output = books_map[book_name].print_book()  # get the book details as string
            return render(request, 'orders/add_order.html', {'form': form, 'book': book_output})
    else:
        form = AddOrderForm()
    return render(request, 'orders/add_order.html', {'form': form})

def delete_order(request):
    book_output = None
    if request.method == 'POST':
        form = DeleteOrderForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            for book_name, book in books_map.items():
                if any(order for order in book.buy_orders + book.sell_orders if order.order_id == order_id):
                    book.delete_order(order_id)
                    book_output = book.print_book()
                    break
            if not book_output:
                book_output = "Order not found."
            return render(request, 'orders/delete_order.html', {'form': form, 'book': book_output})
    else:
        form = DeleteOrderForm()

    return render(request, 'orders/delete_order.html', {'form': form, 'book': book_output})

def home(request):
    return render(request, 'orders/home.html')

# def order_management(request):
#     book_output = None
#     add_form = AddOrderForm(request.POST or None, prefix='add')
#     delete_form = DeleteOrderForm(request.POST or None, prefix='delete')
#     if request.method == 'POST':
#         # Adding an Order
#         if 'add_order' in request.POST and add_form.is_valid():
#             book_name = add_form.cleaned_data['book']
#             order_ = Order(
#                 book=book_name,
#                 operation=add_form.cleaned_data['operation'],
#                 price=add_form.cleaned_data['price'],
#                 volume=add_form.cleaned_data['volume'],
#                 order_id=add_form.cleaned_data['order_id']
#             )
#             books_map[book_name].add_order(order_)
#             book_output = books_map[book_name].print_book()
#             add_form = AddOrderForm(prefix='add')
#         elif 'delete_order' in request.POST and delete_form.is_valid():
#             order_id = delete_form.cleaned_data['order_id']
#             for book_name, book in books_map.items():
#                 if any(order for order in book.buy_orders + book.sell_orders if order.order_id == order_id):
#                     book.delete_order(order_id)
#                     book_output = book.print_book()
#                     break
#
#             if not book_output:
#                 book_output = "Order not found."
#             delete_form = DeleteOrderForm(prefix='delete')
#
#     context = {
#         'add_form': add_form,
#         'delete_form': delete_form,
#         'book_output': book_output,
#     }
#
#     return render(request, 'orders/home.html', context)