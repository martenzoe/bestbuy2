# Store Management System

## Description

The Store Management System is a simple command-line application that allows users to manage a store's inventory. Users can view products, check total quantities, place orders, and manage promotions. The application is designed to be user-friendly and provides a menu-driven interface for easy navigation.

## Features

- **List Active Products:** View all active products in the store.
- **Total Quantity:** Display the total quantity of products available in the store.
- **Place Orders:** Place orders for products with specified quantities and view the total price, including any applied promotions.
- **Product Management:** Handle product activation and deactivation based on inventory levels.
- **Non-Stocked and Limited Products:** Support for specialized product types like non-stocked and limited-quantity items.
- **Promotions:** Apply various promotions, such as:
  - Second item at half price.
  - Buy two, get one free.
  - Percentage discounts.

## Requirements

- Python 3.6 or higher

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/store-management-system.git
   cd store-management-system
   ```

2. Install dependencies:

   If there are additional dependencies, ensure they are listed in a `requirements.txt` file. Install them using:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   Navigate to the directory where your script is located and run:

   ```bash
   python main.py
   ```

2. Interact with the menu:

   Once the application starts, you will see a menu with the following options:

   ```text
   1. List all products in store
   2. Show total amount in store
   3. Make an order
   4. Quit
   ```

3. Choose an option by entering the corresponding number:

   - To list all products, select option `1`.
   - To view the total quantity of products, select option `2`.
   - To place an order, select option `3` and follow the prompts.
   - To exit the program, select option `4`.

## Example

Here’s an example of how to use the application:

1. Start the application.
2. Choose option `1` to list all products.
3. Choose option `2` to see the total quantity available.
4. Choose option `3` to place an order by entering product names and quantities.
5. Finally, choose option `4` to quit the application.

## Testing

Unit tests for the application are written using `pytest`. To execute the tests:

1. Ensure `pytest` is installed:

   ```bash
   pip install pytest
   ```

2. Run the tests:

   ```bash
   pytest
   ```

3. Check the results to ensure all tests pass successfully.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.
