import json
import random
import string
import sqlite3
from difflib import get_close_matches

# Global cart
cart = []

# ---------- TEXT CLEAN ----------
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# ---------- LOAD INTENTS ----------
def load_data():
    with open("intents.json") as file:
        return json.load(file)

# ---------- INTENT MATCH ----------
def get_intent_response(user_input):
    data = load_data()
    user_input = preprocess(user_input)

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern in user_input:
                return random.choice(intent["responses"])
    return None

# ---------- FUZZY PRODUCT MATCH ----------
def match_product(user_input, products):
    names = [p[0].lower() for p in products]
    matches = get_close_matches(user_input, names, n=1, cutoff=0.6)
    return matches[0] if matches else None

# ---------- MAIN RESPONSE ----------
def get_response(user_input):
    user_input = preprocess(user_input)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT name, price FROM products")
    products = cur.fetchall()

    # ----- ADD TO CART -----
    for name, price in products:
        if name.lower() in user_input:
            cart.append((name, price))
            return f"✅ {name} added to cart 🛒"

    # ----- FUZZY MATCH -----
    match = match_product(user_input, products)
    if match:
        for name, price in products:
            if name.lower() == match:
                cart.append((name, price))
                return f"✅ {name} added to cart 🛒"

    # ----- SHOW CART -----
    if "cart" in user_input:
        if not cart:
            return "🛒 Your cart is empty"

        response = "🛒 Your Cart:\n"
        total = 0

        for item in cart:
            price = int(item[1].replace("₹", ""))
            response += f"{item[0]} - ₹{price}\n"
            total += price

        response += f"\nTotal: ₹{total}"
        return response

    # ----- CHECKOUT -----
    if "checkout" in user_input:
        cart.clear()
        return "✅ Order placed successfully!"

    # ----- INTENTS -----
    intent_reply = get_intent_response(user_input)
    if intent_reply:
        return intent_reply

    # ----- FALLBACK -----
    return "🤔 I didn’t understand that. Try asking about products, cart, or orders."
