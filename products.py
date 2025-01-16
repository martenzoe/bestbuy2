from abc import ABC, abstractmethod


class Product:
    """
    Represents a product with attributes such as name, price, and quantity.
    Handles operations like activation, promotion, and purchasing.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initialize a new product.

        :param name: The name of the product.
        :param price: The price of the product.
        :param quantity: The available quantity of the product.
        :raises ValueError: If name is empty, price is negative, or quantity is negative.
        """
        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True  # active is set to True by default
        self.promotion = None  # Initialize promotion as None

    def get_quantity(self) -> float:
        """
        Get the current quantity of the product.

        :return: The current quantity as a float.
        """
        return float(self.quantity)

    def set_quantity(self, quantity: int):
        """
        Set a new quantity for the product.

        :param quantity: The new quantity to set.
        :raises ValueError: If the new quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """
        Check if the product is active.

        :return: True if the product is active, False otherwise.
        """
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def set_promotion(self, promotion):
        """
        Set a promotion for the product.

        :param promotion: The promotion to apply to the product.
        """
        self.promotion = promotion

    def remove_promotion(self):
        """Remove the promotion from the product."""
        self.promotion = None

    def show(self) -> str:
        """
        Get a string representation of the product.

        :return: A string containing the product's name, price, and quantity.
                 Includes promotion information if applicable.
        """
        promo_info = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_info}"

    def buy(self, quantity: int) -> float:
        """
        Buy a specified quantity of the product.

        :param quantity: The quantity to purchase.
        :return: The total price for the purchase.
        :raises ValueError: If quantity is invalid, the product is inactive, or stock is insufficient.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if not self.active:
            raise ValueError("Product is not active")

        if quantity > self.quantity:
            raise ValueError("Not enough stock available")

        # Calculate total price considering promotions
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        # Reduce stock based on purchased items
        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return float(total_price)


class NonStockedProduct(Product):
    """Represents a product that is always non-stocked."""

    def __init__(self, name: str, price: float):
        """
        Initialize a non-stocked product.

        :param name: The name of the product.
        :param price: The price of the product.
        """
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int):
        """Override to keep quantity always at 0."""
        pass

    def show(self) -> str:
        """
        Get a string representation of the non-stocked product.

        :return: A string containing the product's name and price.
        """
        return f"{self.name}, Price: {self.price}, Non-stocked product"


class LimitedProduct(Product):
    """Represents a product with a purchase limit per order."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initialize a limited product.

        :param name: The name of the product.
        :param price: The price of the product.
        :param quantity: The available quantity of the product.
        :param maximum: The maximum quantity that can be purchased in a single order.
        """
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """
        Buy a specified quantity of the limited product.

        :param quantity: The quantity to purchase.
        :return: The total price for the purchase.
        :raises ValueError: If the quantity exceeds the maximum limit.
        """
        if quantity > self.maximum:
            raise ValueError(f"Cannot buy more than {self.maximum} of {self.name}")
        return super().buy(quantity)

    def show(self) -> str:
        """
        Get a string representation of the limited product.

        :return: A string containing the product's name, price, quantity, and maximum per order.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum per order: {self.maximum}"


class Promotion(ABC):
    """Abstract base class for promotions."""

    def __init__(self, name: str):
        """
        Initialize a promotion.

        :param name: The name of the promotion.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the promotion to a product for a specified quantity.

        :param product: The product to which the promotion applies.
        :param quantity: The quantity of the product being purchased.
        :return: The total price after applying the promotion.
        """
        pass


class PercentageDiscount(Promotion):
    """Represents a percentage discount promotion."""

    def __init__(self, name: str, percent: float):
        """
        Initialize a percentage discount promotion.

        :param name: The name of the promotion.
        :param percent: The discount percentage.
        """
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the percentage discount to the product.

        :param product: The product to which the promotion applies.
        :param quantity: The quantity of the product being purchased.
        :return: The total price after applying the discount.
        """
        total_price = product.price * quantity
        discount_amount = total_price * (self.percent / 100)
        return total_price - discount_amount


class SecondItemHalfPrice(Promotion):
    """Represents a promotion where the second item is half price."""

    def __init__(self):
        """Initialize the second item half price promotion."""
        super().__init__("Second Item at Half Price")

    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the second item half price promotion to the product.

        :param product: The product to which the promotion applies.
        :param quantity: The quantity of the product being purchased.
        :return: The total price after applying the promotion.
        """
        if quantity < 1:
            return product.price * quantity

        total_price = 0.0
        pairs = quantity // 2
        total_price += pairs * (product.price + (product.price / 2))
        remainder = quantity % 2
        total_price += remainder * product.price

        return total_price


class BuyTwoGetOneFree(Promotion):
    """Represents a promotion where every third item is free."""

    def __init__(self):
        """Initialize the buy two, get one free promotion."""
        super().__init__("Buy 2, Get 1 Free")

    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the buy two, get one free promotion to the product.

        :param product: The product to which the promotion applies.
        :param quantity: The quantity of the product being purchased.
        :return: The total price after applying the promotion.
        """
        if quantity < 1:
            return product.price * quantity

        free_items = quantity // 3
        payable_items = quantity - free_items

        return product.price * payable_items
