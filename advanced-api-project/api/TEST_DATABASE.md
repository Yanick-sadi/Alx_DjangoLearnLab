# Test Database Configuration

## Overview
This project is configured to use a separate test database to ensure that test operations do not impact development or production data.

## Configuration
The test database is configured in `advanced_api_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }
}