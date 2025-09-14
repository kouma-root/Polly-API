"""
User Registration Module for Polly API

This module provides functions to register new users via the Polly API's /register endpoint.
It handles user registration with proper error handling and follows the OpenAPI specification.

Functions:
    register_user: Main function to register a user with exception handling
    register_user_with_error_handling: Convenience function that returns None on failure

Example:
    # Basic usage
    try:
        user_data = register_user("testuser", "testpassword123")
        print(f"User registered: {user_data}")
    except Exception as e:
        print(f"Error: {e}")
    
    # With error handling
    user_data = register_user_with_error_handling("user", "pass")
    if user_data:
        print("Registration successful")
"""

import requests
import json
from typing import Dict, Any, Optional


def register_user(username: str, password: str, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Register a new user via the /register endpoint.
    
    Args:
        username (str): The username for the new user
        password (str): The password for the new user
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Dict[str, Any]: The response data containing user information on success
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the registration fails (e.g., username already exists)
    """
    url = f"{base_url}/register"
    
    # Prepare the request data according to UserCreate schema
    data = {
        "username": username,
        "password": password
    }
    
    # Set headers for JSON content
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the user data (UserOut schema)
            return response.json()
        elif response.status_code == 400:
            # Username already registered
            error_msg = "Username already registered"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = error_data["detail"]
            except json.JSONDecodeError:
                pass
            raise ValueError(f"Registration failed: {error_msg}")
        else:
            # Other error status codes
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


def register_user_with_error_handling(username: str, password: str, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Register a new user with basic error handling that returns None on failure.
    
    Args:
        username (str): The username for the new user
        password (str): The password for the new user
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Optional[Dict[str, Any]]: The response data on success, None on failure
    """
    try:
        return register_user(username, password, base_url)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Registration failed: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Example 1: Basic usage with exception handling
    try:
        user_data = register_user("testuser", "testpassword123")
        print(f"User registered successfully: {user_data}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Usage with error handling function
    user_data = register_user_with_error_handling("anotheruser", "anotherpassword123")
    if user_data:
        print(f"User registered successfully: {user_data}")
    else:
        print("Registration failed")
