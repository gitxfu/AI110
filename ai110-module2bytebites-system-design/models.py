# ByteBites Backend Models
# Classes: MenuItem, Customer, Menu, Order


class MenuItem:
    """A single food item sold by ByteBites."""

    def __init__(self, name: str, price: float, category: str, popularity_rating: int):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating


class Customer:
    """A ByteBites customer with purchase history."""

    def __init__(self, name: str, purchase_history: list = None):
        self.name = name
        self.purchase_history = purchase_history if purchase_history is not None else []

    def is_verified(self) -> bool:
        """A customer is verified if they have at least one past order."""
        return len(self.purchase_history) > 0


class Menu:
    """A collection of MenuItems that supports filtering."""

    def __init__(self, items: list = None):
        self.items = items if items is not None else []

    def filter_by_category(self, category: str) -> list:
        """Return all items matching the given category (case-insensitive)."""
        return [item for item in self.items if item.category.lower() == category.lower()]


class Order:
    """A transaction grouping selected MenuItems."""

    def __init__(self, items: list = None):
        self.items = items if items is not None else []

    def get_total(self) -> float:
        """Compute the total cost of all items in the order."""
        return sum(item.price for item in self.items)
