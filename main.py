from products import Product, NonStockedProduct, LimitedProduct, SecondItemHalfPrice, BuyTwoGetOneFree, PercentageDiscount
from store import Store


def start(store):
    """
    Start the interactive menu for the store.

    :param store: The Store object to interact with.
    """
    while True:
        print("\nMenu:")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose an option (1-4): ")

        if choice == '1':
            # List all products
            try:
                products = store.get_all_products()
                print("\nProducts in Store:")
                for product in products:
                    print(product.show())
            except ValueError as e:
                print(e)

        elif choice == '2':
            # Show total amount in store
            total_quantity = store.get_total_quantity()
            print(f"\nTotal amount of products in store: {total_quantity}")

        elif choice == '3':
            # Make an order
            order_list = []
            while True:
                product_name = input("Enter product name (or type 'done' to finish): ")
                if product_name.lower() == 'done':
                    break

                try:
                    quantity = int(input(f"Enter quantity for {product_name}: "))
                except ValueError:
                    print("Please enter a valid integer for quantity.")
                    continue

                # Find the product in the store
                product = next((p for p in store.products if p.name == product_name), None)
                if product:
                    order_list.append((product, quantity))
                else:
                    print("Product not found.")

            try:
                total_price = store.order(order_list)
                print(f"Total price of your order: {total_price:.2f}")
            except ValueError as e:
                print(e)

        elif choice == '4':
            print("Thank you for visiting the store!")
            break  # Exit the loop and quit

        else:
            print("Invalid choice. Please select a valid option.")


def main():
    """
    Main function to set up the initial inventory and start the store menu.
    """
    # Setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    # Create promotion catalog
    second_half_price = SecondItemHalfPrice()  # Instanziierung ohne Parameter
    third_one_free = BuyTwoGetOneFree()  # Instanziierung ohne Parameter
    thirty_percent = PercentageDiscount("30% off!", percent=30)
  # Instanziierung mit Name und Prozent

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)  # Setzt die zweite Artikel zum halben Preis auf das erste Produkt
    product_list[1].set_promotion(third_one_free)  # Setzt "Kaufe zwei, bekomme einen kostenlos" auf das zweite Produkt
    product_list[2].set_promotion(thirty_percent)  # Setzt den 30%-Rabatt auf das dritte Produkt

    # Create a store with the initial product list
    best_buy = Store(product_list)

    # Start the interactive menu
    start(best_buy)


if __name__ == "__main__":
    main()
