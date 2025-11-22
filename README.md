# niner-exchange-api

A Django REST Framework API for the Niner Exchange marketplace platform, enabling UNC Charlotte students to buy, sell, and trade items, textbooks, subleases, and services.

## Features

- **User Authentication**: JWT-based authentication with email verification
- **Multi-type Listings**: Support for items, textbooks, subleases, and services
- **Transaction Management**: Handle offers, acceptances, and completions
- **Review System**: Rate and review users after transactions
- **Price Suggestions**: Integration with eBay API for market price estimates
- **Image Upload**: Cloudinary integration for listing images
- **Real-time Notifications**: Firebase integration for instant updates
- **Admin Dashboard**: Manage reports, exchange zones, and moderate content

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Setup Instructions

### 1. Install PostgreSQL

Make sure PostgreSQL is installed and running on your system. Create a local database for the project:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE "niner-exchange";

# Exit PostgreSQL
\q
```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd niner-exchange-api
```

### 3. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory using `.env.example` as a template:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```env
# Database Configuration
DB_NAME=niner-exchange
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Cloudinary (for image uploads)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# eBay API (for price suggestions)
EBAY_CLIENT_ID=your_ebay_client_id
EBAY_CLIENT_SECRET=your_ebay_client_secret

# SendGrid (for email)
SENDGRID_API_KEY=your_sendgrid_api_key
DEFAULT_FROM_EMAIL=noreply@ninerexchange.com

# Django Settings (optional)
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Set Up Firebase (Required for Real-time Features)

1. Save the key as `firebase-service-account.json` in the project root directory

### 7. Run Database Migrations

```bash
python manage.py migrate
```

### 8. Seed the Database (Optional)

Populate the database with sample data:

```bash
python manage.py seed_db
```

This creates:
- 2 test users
- 1 meetup location
- 4 sample listings (textbook, item, sublease, service)

### 9. Create a Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

### 10. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Documentation

### Authentication Endpoints

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and receive JWT tokens
- `POST /api/auth/logout/` - Logout and blacklist refresh token
- `GET /api/auth/verify-email/<uidb64>/<token>/` - Verify email address
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/get-me/` - Get current user profile

### Listing Endpoints

- `GET /api/listings/` - List all listings (with filters)
- `GET /api/listings/<uuid>/` - Get specific listing details
- `PUT /api/listings/<uuid>/edit/` - Update listing
- `PATCH /api/listings/<uuid>/status/` - Update listing status
- `POST /api/items/` - Create item listing
- `POST /api/textbooks/` - Create textbook listing
- `POST /api/subleases/` - Create sublease listing
- `POST /api/services/` - Create service listing

### Transaction Endpoints

- `POST /api/transactions/` - Create transaction offer
- `GET /api/transactions/<uuid>/` - Get transaction details
- `PATCH /api/transactions/<uuid>/update-status/` - Update transaction status

### Review Endpoints

- `POST /api/reviews/` - Create review
- `GET /api/users/<uuid>/reviews/` - Get user reviews

### Other Endpoints

- `GET /api/users/<uuid>/` - Get user profile
- `GET /api/meetup-locations/` - List meetup locations
- `POST /api/images/` - Upload listing images
- `POST /api/pricing/suggest/` - Get price suggestions from eBay
- `POST /api/reports/create/` - Report content
- `GET /api/health/` - Health check endpoint

## Admin Features

Admin users can access additional endpoints at `/api/admin/`:

- View and manage flagged reports
- Manage exchange zones (meetup locations)
- Access content type information

Admin panel available at: `http://localhost:8000/admin/`

## Project Structure

```
niner-exchange-api/
├── core/                       # Main application
│   ├── models/                # Database models
│   ├── serializers/           # DRF serializers
│   ├── views/                 # API views
│   ├── urls/                  # URL routing
│   ├── services/              # External API integrations
│   └── management/commands/   # Custom management commands
├── niner_exchange_api/        # Project configuration
├── .env.example               # Environment variables template
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## Key Technologies

- **Django 5.2** - Web framework
- **Django REST Framework** - API toolkit
- **PostgreSQL** - Database
- **JWT** - Authentication
- **Cloudinary** - Image storage
- **Firebase** - Real-time notifications
- **SendGrid** - Email service
- **eBay API** - Price suggestions

## Development Notes

- All users must have an `@charlotte.edu` email address
- Email verification is required before account activation
- Multi-table inheritance is used for different listing types
- Signals automatically update user ratings and sold item counts
- eBay API responses are cached for 30 minutes

## Testing

Run tests with:

```bash
python manage.py test
```

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

### Import Errors
- Confirm virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Firebase Errors
- Verify `firebase-service-account.json` exists in project root
- Check Firebase project configuration

### Email Not Sending
- Verify SendGrid API key is valid
- Check `DEFAULT_FROM_EMAIL` is configured
- In development, emails may print to console

## License

This project is part of an academic assignment for UNC Charlotte.

## Contributors

- Add Contributors