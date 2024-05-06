# Vendor Management System with Performance Metrics

This is a Vendor Management System developed using Django and Django REST Framework. The system handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/AmishaGupta3803/vendor-management-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd vendor-management-system
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser to access the admin panel:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints

### Vendors

- `GET /api/vendors/`: List all vendors.
- `POST /api/vendors/`: Create a new vendor.
- `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details.
- `PUT /api/vendors/{vendor_id}/`: Update a vendor's details.
- `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

### Purchase Orders

- `GET /api/purchase_orders/`: List all purchase orders.
- `POST /api/purchase_orders/`: Create a new purchase order.
- `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
- `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.
- `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.

### Vendor Performance Metrics

- `GET /api/vendors/{vendor_id}/performance/`: Retrieve a vendor's performance metrics.
- `POST /api/purchase_orders/{po_id}/acknowledge/`: Update acknowledgment_date of purchase order.

## Authentication

API endpoints are secured with token-based authentication. Obtain a token by sending a POST request to `/api/token/`. Use the obtained token in the `Authorization` header as `Bearer <token>` to authenticate API requests.

## Running Tests

To run the test suite, use the following command:

```bash
python manage.py test
