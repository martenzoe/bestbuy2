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
            raise ValueError("Quantity cannot be empty")

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

    def show(self) -> str:
        """
        Get a string representation of the product.

        :return: A string containing the product's name, price, and quantity.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Purchase a specified quantity of the product.

        :param quantity: The quantity to purchase.
        :return: The total price for the purchased quantity.
        :raises ValueError: If the requested quantity is non-positive,
                            exceeds available stock, or if the product is not active.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if quantity > self.quantity:
            raise ValueError("Not enough stock available")

        if not self.active:
            raise ValueError("Product is not active")

        total_price = quantity * self.price
        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return float(total_price)
