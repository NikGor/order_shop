[![Github Actions Status](https://github.com/NikGor/order_shop/workflows/Python%20CI/badge.svg)](https://github.com/NikGor/order_shop/actions)

# OrderShop

OrderShop is a Django-based application designed to monitor the status of orders and shops, and send notifications to an external API when certain conditions are met.

### Prerequisites

- Python 3.7+
- Poetry

## Configuration

1. Create a `.env` file in the project root according to the `.env_example` file and add your configuration variables.

2. Ensure the `.env` file is included in your `.gitignore` to keep it out of version control.

## Usage

1. Run the Django development server:
    ```bash
    poetry run python manage.py runserver
    ```

2. Access the application at `http://127.0.0.1:8000/`.

3. Use the Django admin interface to manage orders and shops.

4. For API documentation, visit `http://127.0.0.1:8000/docs`.

## License

This project is licensed under the MIT License.
