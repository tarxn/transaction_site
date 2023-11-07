from django.db import models

# Create your models here.
import xml.etree.ElementTree as ET
from datetime import datetime
import time
from itertools import zip_longest
import bisect

class Order:
    def __init__(self, book, operation, price, volume, order_id):
        self.book = book
        self.operation = operation.upper()  # BUY or SELL
        self.price = float(price)
        self.volume = int(volume)
        self.order_id = order_id
        self.timestamp = time.time()

    def __lt__(self, other):
        if self.price == other.price:
            return self.timestamp < other.timestamp
        if self.operation == "BUY":
            return self.price > other.price
        return self.price < other.price


class Book:
    def __init__(self, name):
        self.name = name
        self.buy_orders = []
        self.sell_orders = []
        # self.order_id_map= {}

    def add_order(self, order):
        if order.operation == "BUY":
            self.match_order(order, self.sell_orders)
            if order.volume > 0:
                index = bisect.bisect_left(self.buy_orders, order, hi=len(self.buy_orders))
                self.buy_orders.insert(index, order)
                # self.order_id_map[order.order_id] = (index, "BUY")
        elif order.operation == "SELL":
            self.match_order(order, self.buy_orders)
            if order.volume > 0:
                index = bisect.bisect_left(self.sell_orders, order, hi=len(self.sell_orders))
                self.sell_orders.insert(index, order)
                # self.order_id_map[order.order_id] = (index,"SELL")

    def delete_order(self, order_id):
        self.buy_orders = [order for order in self.buy_orders if order.order_id != order_id]
        self.sell_orders = [order for order in self.sell_orders if order.order_id != order_id]

    def match_order(self, new_order, current_orders):
        index = 0
        while index < len(current_orders) and new_order.volume > 0:
            current_order = current_orders[index]
            is_buy = new_order.operation == "BUY" and new_order.price >= current_order.price
            is_sell = new_order.operation == "SELL" and new_order.price <= current_order.price
            if is_buy or is_sell:
                traded_volume = min(new_order.volume, current_order.volume)
                new_order.volume -= traded_volume
                current_order.volume -= traded_volume

                if current_order.volume == 0:
                    current_orders.pop(index)
                    # self.order_id_map.pop(current_order.order_id, None)
                else:
                    index += 1
            else:
                break

    def print_book(self):
        output = []
        max_len = 15
        longest_buy = max((len(f"{b.volume}@{b.price}") for b in self.buy_orders), default=0)
        longest_sell = max((len(f"{s.volume}@{s.price}") for s in self.sell_orders), default=0)
        column_width = max(max_len, longest_buy, longest_sell)
        output.append(f"book: {self.name}")
        output.append("           Buy   --   Sell")
        output.append("=" * (column_width * 2 + 5))
        for b, s in zip_longest(self.buy_orders, self.sell_orders, fillvalue=""):
            b_str = f"{b.volume}@{b.price}" if b else ""
            s_str = f"{s.volume}@{s.price}" if s else ""
            output.append(f" {b_str:^{column_width}} -- {s_str:^{column_width}}")
        return '\n'.join(output)


book1 = Book("book-1")
book2 = Book("book-2")
book3 = Book("book-3")

books_map = {
    "book-1": book1,
    "book-2": book2,
    "book-3": book3
}

# start_time = datetime.now()
# print(f"Processing started at: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
#
# # for order in root:
# #     if order.tag == 'AddOrder':
# #         order_ = Order(
# #             order.attrib['book'],
# #             order.attrib['operation'],
# #             float(order.attrib['price']),
# #             int(order.attrib['volume']),
# #             int(order.attrib['orderId'])
# #         )
# #         books_map[order.attrib['book']].add_order(order_)
# #     else:
# #         books_map[order.attrib['book']].delete_order(int(order.attrib['orderId']))
#
# book1.print_book()
# book2.print_book()
# book3.print_book()
#
# end_time = datetime.now()
# print(f"Processing completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
# print(f"Processing Duration: {(end_time - start_time).total_seconds()} seconds")
