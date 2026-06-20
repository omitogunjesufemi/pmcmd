# PMCMD - PM Command Centre - Governance Tracker

PMCMD is a backend service for tracking governance and initiatives within a project management context. It provides a robust API for managing initiative types, stages, requirements, and document approvals with built-in audit logging.

## Tech Stack

- **Language:** Python 3.12+
- **Framework:** [Django 6.0](https://www.djangoproject.com/)
- **API Framework:** [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- **Authentication:** JWT (SimpleJWT)
- **Documentation:** OpenAPI 3 / Swagger (drf-spectacular)
- **Database:** SQLite (default for development)
- **Configuration:** python-decouple

## Prerequisites

- Python 3.12 or higher
- `pip` (Python package manager)
- `virtualenv` or `venv` module

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pmcmd
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Unix/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Optional):**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

Start the development server:
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## API Documentation

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **Schema (YAML):** `http://127.0.0.1:8000/api/schema/`

## Project Structure

```text
pmcmd/
├── api/
│   ├── auth/          # User authentication and management
│   └── core/          # Initiative management, repositories, services, views
├── config/            # Project configuration (settings, urls, asgi/wsgi)
│   └── settings/      # Django settings split (base, dev)
├── utils/             # Shared utilities, exceptions, and constants
├── manage.py          # Django management script
├── requirements.txt   # Project dependencies
└── db.sqlite3         # Local database (generated after migration)
```

## Key Scripts

- **Run Tests:**
  ```bash
  python manage.py test
  ```
- **Make Migrations:**
  ```bash
  python manage.py makemigrations
  ```
- **Check Linting (if configured):**
  - TODO: Add linting script info

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key for security | Mandatory |
| `DEBUG` | Enable/Disable debug mode | `False` |
| `DATABASE_URL` | Database connection string | TODO: Add if switched from SQLite |

## License

TODO: Specify the license (e.g., MIT, Proprietary).
