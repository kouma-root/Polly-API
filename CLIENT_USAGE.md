# Polly API Client Functions

This directory contains client-side functions to interact with the Polly API using the `requests` library.

## Available Modules

### 1. User Registration (`register_user.py`)

Functions to register new users via the `/register` endpoint.

**Main Functions:**
- `register_user(username, password, base_url)` - Register a user with exception handling
- `register_user_with_error_handling(username, password, base_url)` - Register a user, returns None on failure

**Example Usage:**
```python
from register_user import register_user, register_user_with_error_handling

# Basic usage with exception handling
try:
    user_data = register_user("testuser", "testpassword123")
    print(f"User registered: {user_data}")
except Exception as e:
    print(f"Error: {e}")

# Simple usage with error handling
user_data = register_user_with_error_handling("user", "pass")
if user_data:
    print("Registration successful")
```

### 2. Poll Data Fetching (`fetch_polls.py`)

Functions to fetch paginated poll data from the `/polls` endpoint.

**Main Functions:**
- `fetch_polls(skip, limit, base_url)` - Fetch paginated polls with exception handling
- `fetch_polls_with_error_handling(skip, limit, base_url)` - Fetch polls, returns None on failure
- `fetch_all_polls(base_url, batch_size)` - Fetch all polls by making multiple requests
- `print_polls_summary(polls)` - Display poll data in a readable format

**Example Usage:**
```python
from fetch_polls import fetch_polls, fetch_all_polls, print_polls_summary

# Fetch first 10 polls
polls = fetch_polls(skip=0, limit=10)

# Fetch next 10 polls (pagination)
polls = fetch_polls(skip=10, limit=10)

# Fetch all polls automatically
all_polls = fetch_all_polls()

# Display polls in a readable format
print_polls_summary(polls)
```

## Installation

Make sure to install the required dependencies:

```bash
pip install -r requirements.txt
```

## API Endpoints Used

- **POST** `/register` - User registration
- **GET** `/polls` - Fetch paginated polls

## Error Handling

All functions provide two variants:
1. **Exception-based**: Raises exceptions on errors (recommended for production)
2. **Return-based**: Returns None on errors (convenient for simple scripts)

## Response Schemas

The functions return data following the OpenAPI specification:
- User registration returns `UserOut` schema
- Poll fetching returns array of `PollOut` schema objects

## Configuration

Default API base URL is `http://localhost:8000`. You can override this by passing the `base_url` parameter to any function.
