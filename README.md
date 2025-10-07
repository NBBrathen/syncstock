# SyncStock API

A production-ready Inventory and Order Management API built with FastAPI and PostgreSQL.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Product Management** - Full CRUD operations with advanced search and filtering
- **Order Processing** - Automatic inventory tracking and stock management
- **Smart Inventory** - Low stock alerts with configurable thresholds
- **Authentication** - Secure JWT-based user authentication
- **RESTful API** - Clean, well-documented endpoints following REST principles
- **Comprehensive Testing** - 28 automated tests with 93% coverage
- **CI/CD Pipeline** - Automated testing with GitHub Actions
- **Docker Ready** - Full containerization with Docker Compose

## Tech Stack

**Backend Framework:**
- FastAPI - Modern, fast web framework for building APIs
- SQLAlchemy - SQL toolkit and ORM
- Alembic - Database migration tool

**Database:**
- PostgreSQL 15 - Advanced open source database

**Authentication:**
- python-jose - JWT token implementation
- passlib - Password hashing with bcrypt

**Testing & Quality:**
- pytest - Testing framework
- Black - Code formatter
- isort - Import sorter
- flake8 - Style guide enforcement

**DevOps:**
- Docker - Containerization
- GitHub Actions - CI/CD automation

## Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- Python 3.11+ (for local development)
- PostgreSQL 15 (if running without Docker)

### Installation with Docker

1. **Clone the repository**

```bash
git clone https://github.com/NBBrathen/syncstock.git
cd syncstock
```

2. **Create environment file**

```bash
cp .env.example .env
```

Edit `.env` and update the following:

```env
SECRET_KEY=your-super-secret-key-here
POSTGRES_PASSWORD=your-secure-password
```

3. **Start the services**

```bash
docker compose up -d
```

4. **Run database migrations**

```bash
docker compose exec api alembic upgrade head
```

### Access the API

- **API Base URL:** http://localhost:8000
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

### Local Development Setup

1. **Create virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL database**

```bash
createdb syncstock
```

4. **Run migrations**

```bash
alembic upgrade head
```

5. **Start the development server**

```bash
uvicorn app.main:app --reload
```

## API Documentation

### Authentication

#### Register New User

```http
POST /auth/register
Content-Type: application/json
```

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepass123"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded
```

```
username=johndoe&password=securepass123
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### Get Current User

```http
GET /auth/me
Authorization: Bearer <token>
```

### Products

#### List Products

```http
GET /products?skip=0&limit=20
```

#### Search Products

```http
GET /products/search?search=shirt&min_price=20&max_price=50&in_stock_only=true
```

**Query Parameters:**
- `search` - Search by product name
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter
- `in_stock_only` - Show only products with stock > 0
- `skip` - Pagination offset (default: 0)
- `limit` - Items per page (default: 100, max: 1000)

#### Get Low Stock Products

```http
GET /products/low-stock
```

Returns products where current stock is at or below the configured threshold.

#### Get Product by ID

```http
GET /products/{product_id}
```

#### Create Product

```http
POST /products
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "name": "Premium T-Shirt",
  "price": 29.99,
  "stock": 100,
  "low_stock_threshold": 10
}
```

#### Update Product

```http
PATCH /products/{product_id}
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "price": 24.99,
  "stock": 150
}
```

#### Delete Product

```http
DELETE /products/{product_id}
Authorization: Bearer <token>
```

### Orders

#### Create Order

```http
POST /orders
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "customer_name": "Jane Smith",
  "customer_email": "jane@example.com",
  "customer_phone": "555-1234",
  "customer_address": "123 Main St, City, State 12345",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

The system automatically:
- Validates product availability
- Calculates total amount
- Deducts stock quantities
- Creates order with all items

#### List Orders

```http
GET /orders?skip=0&limit=20
```

#### Filter Orders

```http
GET /orders/filter?status=pending&customer_email=jane@example.com
```

**Query Parameters:**
- `status` - Filter by order status
- `customer_email` - Filter by customer email (partial match)
- `skip` - Pagination offset
- `limit` - Items per page

#### Get Order by ID

```http
GET /orders/{order_id}
```

**Response includes full order details with all items:**

```json
{
  "id": 1,
  "customer_name": "Jane Smith",
  "customer_email": "jane@example.com",
  "customer_phone": "555-1234",
  "customer_address": "123 Main St, City, State 12345",
  "order_date": "2024-10-06T12:00:00Z",
  "status": "pending",
  "total_amount": 89.97,
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 2,
      "price_at_purchase": 29.99
    }
  ]
}
```

#### Update Order Status

```http
PATCH /orders/{order_id}/status
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "status": "shipped"
}
```

**Valid statuses:** `pending`, `processing`, `shipped`, `delivered`, `cancelled`

#### Cancel Order

```http
DELETE /orders/{order_id}/cancel
Authorization: Bearer <token>
```

Canceling an order:
- Changes order status to "cancelled"
- Automatically restores product stock
- Cannot be performed on delivered orders

## Development

### Running Migrations

```bash
# Create a new migration
docker compose exec api alembic revision --autogenerate -m "description"

# Apply migrations
docker compose exec api alembic upgrade head

# Rollback one migration
docker compose exec api alembic downgrade -1

# View migration history
docker compose exec api alembic history
```

### Code Formatting

```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Check style with flake8
flake8 app/ tests/ --max-line-length=120
```

### Viewing Logs

```bash
# View API logs
docker compose logs -f api

# View database logs
docker compose logs -f db

# View all logs
docker compose logs -f
```

### Accessing the Database

```bash
# Connect to PostgreSQL
docker compose exec db psql -U syncstock -d syncstock

# Common SQL commands
\dt          # List tables
\d products  # Describe products table
SELECT * FROM products LIMIT 10;
```

## Testing

The project includes comprehensive automated tests covering authentication, products, and orders.

### Run Tests

```bash
# Run tests locally
pytest tests/ -v

# Run tests in Docker
docker compose exec api pytest tests/ -v
```

### Test Coverage

```bash
# Generate coverage report
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Coverage Statistics

- **Current test coverage:** 93%
- **Coverage by module:**
  - Authentication: 95%
  - Products: 94%
  - Orders: 92%
  - CRUD operations: 90%

### Continuous Integration

Every push and pull request automatically:
- Runs all 28 tests
- Checks code coverage
- Validates code formatting
- Runs linting checks

## Project Structure

```
syncstock/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
│
├── alembic/
│   ├── versions/               # Database migration files
│   └── env.py                  # Alembic configuration
│
├── app/
│   ├── routers/               # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── orders.py          # Order management endpoints
│   │   └── products.py        # Product management endpoints
│   │
│   ├── __init__.py
│   ├── auth.py                # JWT authentication logic
│   ├── crud.py                # Database CRUD operations
│   ├── database.py            # Database connection setup
│   ├── dependencies.py        # Shared dependencies
│   ├── main.py                # FastAPI application entry point
│   ├── models.py              # SQLAlchemy ORM models
│   └── schemas.py             # Pydantic request/response schemas
│
├── tests/
│   ├── conftest.py            # Pytest fixtures and configuration
│   ├── test_auth.py           # Authentication tests
│   ├── test_orders.py         # Order management tests
│   └── test_products.py       # Product management tests
│
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── alembic.ini                # Alembic configuration
├── docker-compose.yml         # Docker services definition
├── Dockerfile                 # Container definition
├── pyproject.toml             # Python project configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/ -v`)
5. Format code (`black app/ tests/ && isort app/ tests/`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Contribution Guidelines

All contributions must:
- Pass all tests
- Maintain or improve code coverage
- Follow existing code style (Black + isort)
- Include tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

**Noel Brady**
- GitHub: [@NBBrathen](https://github.com/NBBrathen)
- LinkedIn: [@NBrathen](https://www.linkedin.com/in/noel-brathen)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Inspired by modern e-commerce and inventory management systems
- Thanks to the open-source community for the excellent tools and libraries