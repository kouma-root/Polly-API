"""
Poll Data Fetching Module for Polly API

This module provides functions to fetch paginated poll data from the Polly API's /polls endpoint.
It supports both single-page fetching and complete data retrieval with proper error handling.

Functions:
    fetch_polls: Main function to fetch paginated polls with exception handling
    fetch_polls_with_error_handling: Convenience function that returns None on failure
    fetch_all_polls: Utility function to fetch all polls by making multiple requests
    print_polls_summary: Helper function to display poll data in a readable format

Example:
    # Fetch first 10 polls
    polls = fetch_polls(skip=0, limit=10)
    
    # Fetch all polls
    all_polls = fetch_all_polls()
    
    # Display polls
    print_polls_summary(polls)
"""

import requests
import json
from typing import Dict, Any, List, Optional


def fetch_polls(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> List[Dict[str, Any]]:
    """
    Fetch paginated poll data from the /polls endpoint.
    
    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        List[Dict[str, Any]]: List of poll objects following the PollOut schema
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the response is not valid
    """
    url = f"{base_url}/polls"
    
    # Prepare query parameters
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            polls_data = response.json()
            
            # Validate that we received a list
            if not isinstance(polls_data, list):
                raise ValueError("Expected a list of polls, but received a different data type")
            
            return polls_data
        else:
            # Handle error status codes
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


def fetch_polls_with_error_handling(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> Optional[List[Dict[str, Any]]]:
    """
    Fetch paginated poll data with basic error handling that returns None on failure.
    
    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Optional[List[Dict[str, Any]]]: List of poll objects on success, None on failure
    """
    try:
        return fetch_polls(skip, limit, base_url)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Failed to fetch polls: {e}")
        return None


def fetch_all_polls(base_url: str = "http://localhost:8000", batch_size: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch all polls by making multiple paginated requests.
    
    Args:
        base_url (str): The base URL of the API (default: "http://localhost:8000")
        batch_size (int): Number of polls to fetch per request (default: 10)
    
    Returns:
        List[Dict[str, Any]]: Complete list of all polls
    """
    all_polls = []
    skip = 0
    
    while True:
        try:
            polls_batch = fetch_polls(skip=skip, limit=batch_size, base_url=base_url)
            
            # If we get an empty list, we've reached the end
            if not polls_batch:
                break
                
            all_polls.extend(polls_batch)
            
            # If we got fewer polls than requested, we've reached the end
            if len(polls_batch) < batch_size:
                break
                
            skip += batch_size
            
        except Exception as e:
            print(f"Error fetching polls batch starting at {skip}: {e}")
            break
    
    return all_polls


def print_polls_summary(polls: List[Dict[str, Any]]) -> None:
    """
    Print a summary of the fetched polls.
    
    Args:
        polls (List[Dict[str, Any]]): List of poll objects
    """
    if not polls:
        print("No polls found.")
        return
    
    print(f"Found {len(polls)} polls:")
    print("-" * 50)
    
    for poll in polls:
        print(f"ID: {poll.get('id', 'N/A')}")
        print(f"Question: {poll.get('question', 'N/A')}")
        print(f"Created: {poll.get('created_at', 'N/A')}")
        print(f"Owner ID: {poll.get('owner_id', 'N/A')}")
        
        options = poll.get('options', [])
        print(f"Options ({len(options)}):")
        for option in options:
            print(f"  - {option.get('text', 'N/A')} (ID: {option.get('id', 'N/A')})")
        
        print("-" * 50)


# Example usage
if __name__ == "__main__":
    # Example 1: Fetch first 10 polls
    try:
        polls = fetch_polls(skip=0, limit=10)
        print_polls_summary(polls)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Fetch polls with error handling
    polls = fetch_polls_with_error_handling(skip=0, limit=5)
    if polls:
        print(f"Successfully fetched {len(polls)} polls")
        print_polls_summary(polls)
    else:
        print("Failed to fetch polls")
    
    # Example 3: Fetch all polls
    print("\nFetching all polls...")
    all_polls = fetch_all_polls()
    print(f"Total polls found: {len(all_polls)}")
    print_polls_summary(all_polls)
