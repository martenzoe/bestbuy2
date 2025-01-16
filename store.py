class Store:
    def __init__(self, products):
        """
        Initialize a new store with a list of products.

        :param products: A list of Product objects. If None, initializes with an empty list.
        """
        self.products = products if products is not None else []

    def add_product(self, product):
        """
        Add a product to the store.

        :param product: The Product object to be added.
        """
        self.products.append(product)

    def remove_product(self, product):
        """
        Remove a product from the store.

        :param product: The Product object to be removed.
        :raises ValueError: If the product does not exist in the store.
        """
        if product in self.products:
            self.products.remove(product)
        else:
            raise ValueError("Product does not exist")

    def get_total_quantity(self) -> int:
        """
        Get the total number of products in the store.

        :return: The total number of products as an integer.
        """
        return len(self.products)

    def get_all_products(self):
        """
        Get a list of all active products in the store.

        :return: A list of active Product objects.
        :raises ValueError: If there are no active products in the store.
        """
        # List comprehension to collect active products
        active_products = [product for product in self.products if product.is_active()]

        if active_products:  # Check if there are any active products
            return active_products  # Return the list of active products
        else:
            raise ValueError("No active products in the store.")

    def order(self, shopping_list) -> float:
        """
        Process an order based on a shopping list.

        :param shopping_list: A list of tuples where each tuple contains a Product object and its quantity.
        :return: The total price of the order as a float.
        :raises ValueError: If any product is not active, quantity is non-positive,
                           or there is insufficient stock available.
        """
        total_price = 0.0  # Initialize total price

        for product, quantity in shopping_list:  # Loop over the shopping list tuples
            if not product.is_active():  # Check if the product is active
                raise ValueError(f"Product {product.name} is not active.")

            if quantity <= 0:  # Check if quantity is positive
                raise ValueError("Quantity must be positive.")

            if quantity > product.quantity:  # Check if sufficient stock is available
                raise ValueError(
                    f"Not enough stock for {product.name}. Available: {product.quantity}, Requested: {quantity}")

            # Calculate price for the current product
            total_price += product.buy(quantity)  # buy() reduces stock and returns price

        return total_price  # Return total price of the order
