import json
import random
import string

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def load_data():
    with open("intents.json") as file:
        return json.load(file)
def get_response(user_input):
 import sqlite3

# Global cart
cart = []

def get_response(user_input):
    user_input = user_input.lower()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT name, price FROM products")
    products = cur.fetchall()

    # Add to cart
    for name, price in products:
        if name.lower() in user_input:
            cart.append((name, price))
            return f"{name} added to cart 🛒"

    # Show cart
    if "cart" in user_input:
        if not cart:
            return "Your cart is empty"

        response = "🛒 Your Cart:\n"
        total = 0

        for item in cart:
            response += f"{item[0]} - {item[1]}\n"
            total += int(item[1].replace("₹",""))

        response += f"Total: ₹{total}"
        return response

    # Checkout
    if "checkout" in user_input:
        cart.clear()
        return "Order placed successfully ✅"

    return "Sorry, I didn't understand."