import pytest
from products import Product, NonStockedProduct, LimitedProduct


def test_create_normal_product():
    product = Product("Test Product", 10.0, 100)
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.quantity == 100
    assert product.is_active() == True


def test_create_invalid_product():
    with pytest.raises(ValueError):
        Product("", 10.0, 100)  # Empty name
    with pytest.raises(ValueError):
        Product("Test Product", -10.0, 100)  # Negative price
    with pytest.raises(ValueError):
        Product("Test Product", 10.0, -100)  # Negative quantity


def test_product_becomes_inactive_at_zero_quantity():
    product = Product("Test Product", 10.0, 1)
    product.buy(1)
    assert product.is_active() == False


def test_product_purchase():
    product = Product("Test Product", 10.0, 100)
    total_price = product.buy(10)
    assert product.quantity == 90
    assert total_price == 100.0


def test_buy_larger_quantity_than_exists():
    product = Product("Test Product", 10.0, 100)
    with pytest.raises(ValueError):
        product.buy(101)


def test_create_limited_product():
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    assert limited_product.name == "Limited Item"
    assert limited_product.price == 20.0
    assert limited_product.quantity == 50
    assert limited_product.maximum == 5


def test_limited_product_purchase_within_limit():
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    total_price = limited_product.buy(3)
    assert limited_product.quantity == 47
    assert total_price == 60.0


def test_limited_product_purchase_exceeding_limit():
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    with pytest.raises(ValueError):
        limited_product.buy(6)


def test_limited_product_show():
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    assert limited_product.show() == "Limited Item, Price: 20.0, Quantity: 50, Maximum per order: 5"


# Tests für die NonStockedProduct-Klasse
def test_create_non_stocked_product():
    non_stocked_product = NonStockedProduct("Windows License", price=125)
    assert non_stocked_product.name == "Windows License"
    assert non_stocked_product.price == 125
    assert non_stocked_product.quantity == 0


def test_non_stocked_product_show():
    non_stocked_product = NonStockedProduct("Windows License", price=125)
    assert non_stocked_product.show() == "Windows License, Price: 125, Non-stocked product"


def test_non_stocked_product_set_quantity():
    non_stocked_product = NonStockedProduct("Windows License", price=125)

    # Setzen der Menge sollte nichts bewirken und keine Ausnahme auslösen
    non_stocked_product.set_quantity(10)
    assert non_stocked_product.quantity == 0  # Die Menge bleibt immer bei 0