"""Quick manual check for ByteBites class scaffolds."""

from models import MenuItem, Customer, Menu, Order

# --- Create MenuItems ---
burger = MenuItem("Spicy Burger", 8.99, "Entrees", 5)
soda = MenuItem("Large Soda", 2.49, "Drinks", 3)
cake = MenuItem("Chocolate Cake", 5.50, "Desserts", 4)

print("=== MenuItems ===")
print(f"{burger.name} | ${burger.price} | {burger.category} | rating: {burger.popularity_rating}")
print(f"{soda.name}   | ${soda.price} | {soda.category}  | rating: {soda.popularity_rating}")
print(f"{cake.name} | ${cake.price} | {cake.category} | rating: {cake.popularity_rating}")

# --- Menu filtering ---
menu = Menu([burger, soda, cake])
drinks = menu.filter_by_category("Drinks")
desserts = menu.filter_by_category("desserts")  # test case-insensitivity

print("\n=== Menu Filter ===")
print(f"Drinks:   {[item.name for item in drinks]}")
print(f"Desserts: {[item.name for item in desserts]}")

# --- Order total ---
order = Order([burger, soda])
print("\n=== Order ===")
print(f"Items: {[item.name for item in order.items]}")
print(f"Total: ${order.get_total()}")

# --- Empty order ---
empty_order = Order()
print(f"Empty order total: ${empty_order.get_total()}")

# --- Customer verification ---
alice = Customer("Alice")
print("\n=== Customer ===")
print(f"{alice.name} verified? {alice.is_verified()}")
alice.purchase_history.append(order)
print(f"{alice.name} verified after order? {alice.is_verified()}")
