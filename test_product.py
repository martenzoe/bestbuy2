import pytest
from products import Product, NonStockedProduct, LimitedProduct, SecondItemHalfPrice, BuyTwoGetOneFree


def test_create_normal_product():
    """Test creating a normal product with valid attributes."""
    product = Product("Test Product", 10.0, 100)
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.quantity == 100
    assert product.is_active() is True


def test_create_invalid_product():
    """Test creating a product with invalid attributes raises ValueError."""
    with pytest.raises(ValueError):
        Product("", 10.0, 100)  # Empty name
    with pytest.raises(ValueError):
        Product("Test Product", -10.0, 100)  # Negative price
    with pytest.raises(ValueError):
        Product("Test Product", 10.0, -100)  # Negative quantity


def test_product_becomes_inactive_at_zero_quantity():
    """Test that a product becomes inactive when its quantity reaches zero."""
    product = Product("Test Product", 10.0, 1)
    product.buy(1)
    assert product.is_active() is False


def test_product_purchase():
    """Test purchasing a specified quantity of a product."""
    product = Product("Test Product", 10.0, 100)
    total_price = product.buy(10)
    assert product.quantity == 90
    assert total_price == 100.0


def test_buy_larger_quantity_than_exists():
    """Test that buying more than available quantity raises ValueError."""
    product = Product("Test Product", 10.0, 100)
    with pytest.raises(ValueError):
        product.buy(101)


def test_create_limited_product():
    """Test creating a limited product with maximum purchase limit."""
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    assert limited_product.name == "Limited Item"
    assert limited_product.price == 20.0
    assert limited_product.quantity == 50
    assert limited_product.maximum == 5


def test_limited_product_purchase_within_limit():
    """Test purchasing within the limit of a limited product."""
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    total_price = limited_product.buy(3)
    assert limited_product.quantity == 47
    assert total_price == 60.0


def test_limited_product_purchase_exceeding_limit():
    """Test that purchasing exceeding the limit raises ValueError."""
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    with pytest.raises(ValueError):
        limited_product.buy(6)


def test_limited_product_show():
    """Test the string representation of a limited product."""
    limited_product = LimitedProduct("Limited Item", 20.0, 50, maximum=5)
    assert limited_product.show() == "Limited Item, Price: 20.0, Quantity: 50, Maximum per order: 5"


# Tests for the NonStockedProduct class
def test_create_non_stocked_product():
    """Test creating a non-stocked product."""
    non_stocked_product = NonStockedProduct("Windows License", price=125)
    assert non_stocked_product.name == "Windows License"
    assert non_stocked_product.price == 125
    assert non_stocked_product.quantity == 0


def test_non_stocked_product_show():
    """Test the string representation of a non-stocked product."""
    non_stocked_product = NonStockedProduct("Windows License", price=125)
    assert non_stocked_product.show() == "Windows License, Price: 125, Non-stocked product"


def test_non_stocked_product_set_quantity():
    """Test setting quantity on a non-stocked product does not change its quantity."""
    non_stocked_product = NonStockedProduct("Windows License", price=125)

    # Setting the quantity should have no effect and not raise an exception
    non_stocked_product.set_quantity(10)
    assert non_stocked_product.quantity == 0  # The quantity remains at zero


def test_second_item_half_price():
    """Test applying the 'Second Item at Half Price' promotion."""
    product = Product("Test Product", price=100.0, quantity=10)
    discount = SecondItemHalfPrice()
    product.set_promotion(discount)

   # Expecting to pay for two items when purchasing three
    assert product.buy(3) == 250.0  # (100 + (100/2) + 100)


def test_buy_two_get_one_free():
   """Test applying the 'Buy Two Get One Free' promotion."""
   product = Product("Test Product", price=100.0, quantity=10)
   discount = BuyTwoGetOneFree()
   product.set_promotion(discount)

   # Expecting to pay for two items when purchasing three
   assert product.buy(3) == 200.0  # (100 * 2)

