"""pytest tests for ByteBites core behaviors."""

import pytest
from models import MenuItem, Customer, Menu, Order


# --- Fixtures ---
# Reusable MenuItem objects shared across tests.
# pytest injects them automatically when a test function names them as parameters.

@pytest.fixture
def burger():
    # A sample Entrees item with price $8.99 and popularity rating 3
    return MenuItem("Spicy Burger", 8.99, "Entrees", 3)

@pytest.fixture
def soda():
    # A sample Drinks item with price $2.49 and popularity rating 5
    return MenuItem("Large Soda", 2.49, "Drinks", 5)

@pytest.fixture
def tea():
    # A second Drinks item used to test multi-item filtering
    return MenuItem("Iced Tea", 1.99, "Drinks", 2)

@pytest.fixture
def cake():
    # A sample Desserts item used for case-insensitive filter tests
    return MenuItem("Chocolate Cake", 5.50, "Desserts", 4)


# --- Order total tests ---

def test_order_total_with_multiple_items(burger, soda):
    """Happy path: total equals the sum of all item prices.

    $8.99 (burger) + $2.49 (soda) = $11.48
    pytest.approx handles floating-point rounding.
    """
    order = Order()
    order.add_item(burger)
    order.add_item(soda)
    assert order.get_total() == pytest.approx(11.48)

def test_order_total_is_zero_when_empty():
    """Edge case: an order with no items should return $0, not crash."""
    order = Order()
    assert order.get_total() == 0


# --- Menu filter tests ---

def test_filter_by_category_returns_matching_items(soda, tea, burger):
    """Happy path: only items whose category matches the query are returned.

    Menu has 2 Drinks and 1 Entree. Filtering for 'Drinks' should return exactly 2.
    """
    menu = Menu()
    menu.add_item(soda)
    menu.add_item(tea)
    menu.add_item(burger)
    drinks = menu.filter_by_category("Drinks")
    assert len(drinks) == 2
    assert all(item.category == "Drinks" for item in drinks)

def test_filter_by_category_is_case_insensitive(cake):
    """Edge case: filter should work regardless of how the user types the category.

    'desserts' and 'DESSERTS' should both match the stored value 'Desserts'.
    """
    menu = Menu([cake])
    assert len(menu.filter_by_category("desserts")) == 1
    assert len(menu.filter_by_category("DESSERTS")) == 1

def test_filter_by_category_returns_empty_for_no_match(burger):
    """Edge case: filtering for a category that doesn't exist returns an empty list."""
    menu = Menu([burger])
    assert menu.filter_by_category("Drinks") == []
