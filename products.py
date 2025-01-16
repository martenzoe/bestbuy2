from abc import ABC, abstractmethod


class Product:
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
        """Set a promotion for the product."""
        self.promotion = promotion

    def remove_promotion(self):
        """Remove the promotion from the product."""
        self.promotion = None

    def show(self) -> str:
        """
        Get a string representation of the product.

        :return: A string containing the product's name, price, and quantity.
                 Also includes promotion information if applicable.
        """
        promo_info = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_info}"

    def buy(self, quantity: int) -> float:
        """
        Purchase a specified quantity of the product.

        :param quantity: The quantity to purchase.
        :return: The total price for the purchased quantity after applying any promotions.
                  Raises ValueError if conditions are not met.

                  If a promotion exists, it should determine the price using the promotion method apply_promotion.

                  Raises ValueError if requested quantity is non-positive,
                  exceeds available stock, or if the product is not active.

                  If no promotion exists, it calculates based on standard pricing.

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
            # Reduce stock based on purchased items
            self.quantity -= quantity
            return total_price

            # Standard pricing calculation
        total_price = quantity * self.price
        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return float(total_price)

class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int):
        pass  # Überschreiben, um die Menge immer bei 0 zu halten

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Non-stocked product"


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"Cannot buy more than {self.maximum} of {self.name}")
        return super().buy(quantity)

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum per order: {self.maximum}"


class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass

class PercentageDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        total_price = product.price * quantity
        discount_amount = total_price * (self.percent / 100)
        return total_price - discount_amount

class SecondItemHalfPrice(Promotion):
    def __init__(self):
        super().__init__("Second Item at Half Price")

    def apply_promotion(self, product, quantity) -> float:
        # Wenn weniger als 2 Artikel gekauft werden, gibt es keinen Rabatt
        if quantity < 1:
            return product.price * quantity

        # Berechnung des Gesamtpreises unter Berücksichtigung des Rabatts
        total_price = 0.0

        # Für jedes Paar von Artikeln: das erste zum vollen Preis, das zweite zum halben Preis
        pairs = quantity // 2
        total_price += pairs * (product.price + (product.price / 2))  # Preis für Paare

        # Überbleibende Artikel (ungerade Anzahl)
        remainder = quantity % 2
        total_price += remainder * product.price  # Preis für verbleibende Artikel

        return total_price


class BuyTwoGetOneFree(Promotion):
    def __init__(self):
        super().__init__("Buy 2, Get 1 Free")

    def apply_promotion(self, product, quantity) -> float:
        free_items = quantity // 3
        payable_items = quantity - free_items
        return product.price * payable_items
