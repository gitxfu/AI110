"""Manual check for ByteBites — covers adding items, sorting, filtering, and totals."""

from models import MenuItem, Customer, Menu, Order

# 1. Adding items — build a menu using add_item
menu = Menu()
menu.add_item(MenuItem("Spicy Burger", 8.99, "Entrees", 3))
menu.add_item(MenuItem("Large Soda", 2.49, "Drinks", 5))
menu.add_item(MenuItem("Chocolate Cake", 5.50, "Desserts", 4))
menu.add_item(MenuItem("Iced Tea", 1.99, "Drinks", 2))

print("=== Adding Items ===")
print(f"Menu has {len(menu.items)} items: {[item.name for item in menu.items]}")

# 2. Sorting menus — by popularity, highest first
ranked = menu.sort_by_popularity()

print("\n=== Sorting ===")
print(f"By popularity: {[f'{i.name}({i.popularity_rating})' for i in ranked]}")

# 3. Filtering categories
drinks = menu.filter_by_category("Drinks")
desserts = menu.filter_by_category("desserts")  # case-insensitive

print("\n=== Filtering ===")
print(f"Drinks:   {[item.name for item in drinks]}")
print(f"Desserts: {[item.name for item in desserts]}")

# 4. Computing an order total
order = Order()
order.add_item(menu.items[0])  # Burger
order.add_item(menu.items[1])  # Soda

print("\n=== Order Total ===")
print(f"Items: {[item.name for item in order.items]}")
print(f"Total: ${order.get_total()}")

# Empty order edge case
empty_order = Order()
print(f"Empty order total: ${empty_order.get_total()}")

# Customer verification via add_order
alice = Customer("Alice")
print("\n=== Customer ===")
print(f"{alice.name} verified? {alice.is_verified()}")
alice.add_order(order)
print(f"{alice.name} verified after order? {alice.is_verified()}")
