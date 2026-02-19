print("----------------------------------------")
print("SHOPPING CART SNAPSHOT")
print("----------------------------------------")
print()

product1 = {
    "info": ("Smartphone", "Electronics"),
    "price": 3000,
    "ratings": [4, 5, 4],
    "tags": {"wireless", "portable", "new"}
}

product2 = {
    "info": ("Laptop", "Electronics"),
    "price": 4500,
    "ratings": [5, 4, 5],
    "tags": {"gaming", "premium", "wireless"}
}

product3 = {
    "info": ("Backpack", "Accessories"),
    "price": 1000,
    "ratings": [4, 4, 3],
    "tags": {"budget", "portable", "new"}
}

cart = [product1, product2, product3]

print(f"Cart contains {len(cart)} products.\n")


print("1. Category of the second product:")
print(cart[1]["info"][1])
print()


total_price = 0
for i in cart:
    total_price += i["price"]
print("2. Total price of all products:")
print(total_price)
print()

avg_rating = sum(cart[0]["ratings"]) / len(cart[0]["ratings"])
print("3. Average rating of the first product:")
print(round(avg_rating, 1))
print()

combined_tags = cart[0]["tags"] | cart[1]["tags"] | cart[2]["tags"]
print("4. Combined tags from all products:")
print(combined_tags)
print()


print("5. Adding a new product (product4)...\n")

product4 = {
    "info": ("Headphones", "Accessories"),
    "price": 3000,
    "ratings": [4, 5, 4],
    "tags": {"audio", "wireless", "music"}
}

cart.append(product4)

print("New product added successfully!\n")

print("Updated Cart Details:")
print("----------------------------------------\n")

print(f"Total products in cart: {len(cart)}\n")

count = 0
for product in cart:
    count+=1
    print(f"Product {count}:")
    print(f"Name: {product['info'][0]}")
    print(f"Category: {product['info'][1]}")
    print(f"Price: {product['price']}")
    print(f"Ratings: {product['ratings']}")
    print(f"Tags: {product['tags']}\n")

print("----------------------------------------")
print("PROGRAM COMPLETED SUCCESSFULLY")
print("----------------------------------------")
