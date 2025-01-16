import pytest
from products import Product


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