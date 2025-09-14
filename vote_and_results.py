"""
Voting and Results Module for Polly API

This module provides functions to cast votes on polls and retrieve poll results
from the Polly API. It handles authentication and follows the OpenAPI specification.

Functions:
    cast_vote: Main function to cast a vote on a poll with JWT authentication
    cast_vote_with_error_handling: Convenience function that returns None on failure
    get_poll_results: Function to retrieve poll results and vote counts
    get_poll_results_with_error_handling: Convenience function that returns None on failure

Example:
    # Cast a vote (requires JWT token)
    try:
        vote_data = cast_vote(poll_id=1, option_id=2, token="your_jwt_token")
        print(f"Vote cast: {vote_data}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Get poll results
    results = get_poll_results(poll_id=1)
    if results:
        print(f"Poll results: {results}")
"""

import requests
import json
from typing import Dict, Any, Optional, List


def cast_vote(poll_id: int, option_id: int, token: str, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Cast a vote on an existing poll via the /polls/{poll_id}/vote endpoint.
    
    Args:
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        token (str): JWT authentication token
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Dict[str, Any]: The response data containing vote information (VoteOut schema)
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the vote fails (e.g., poll/option not found, unauthorized)
    """
    url = f"{base_url}/polls/{poll_id}/vote"
    
    # Prepare the request data according to VoteCreate schema
    data = {
        "option_id": option_id
    }
    
    # Set headers for JSON content and JWT authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the vote data (VoteOut schema)
            return response.json()
        elif response.status_code == 401:
            raise ValueError("Unauthorized: Invalid or missing JWT token")
        elif response.status_code == 404:
            raise ValueError("Poll or option not found")
        else:
            # Other error status codes
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


def cast_vote_with_error_handling(poll_id: int, option_id: int, token: str, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Cast a vote with basic error handling that returns None on failure.
    
    Args:
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        token (str): JWT authentication token
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Optional[Dict[str, Any]]: The response data on success, None on failure
    """
    try:
        return cast_vote(poll_id, option_id, token, base_url)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Vote failed: {e}")
        return None


def get_poll_results(poll_id: int, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Retrieve poll results via the /polls/{poll_id}/results endpoint.
    
    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Dict[str, Any]: The response data containing poll results (PollResults schema)
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the poll is not found
    """
    url = f"{base_url}/polls/{poll_id}/results"
    
    try:
        # Make the GET request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the results data (PollResults schema)
            return response.json()
        elif response.status_code == 404:
            raise ValueError("Poll not found")
        else:
            # Other error status codes
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


def get_poll_results_with_error_handling(poll_id: int, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Get poll results with basic error handling that returns None on failure.
    
    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Optional[Dict[str, Any]]: The response data on success, None on failure
    """
    try:
        return get_poll_results(poll_id, base_url)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Failed to get poll results: {e}")
        return None


def print_poll_results(results: Dict[str, Any]) -> None:
    """
    Print poll results in a readable format.
    
    Args:
        results (Dict[str, Any]): Poll results data from get_poll_results
    """
    if not results:
        print("No results available.")
        return
    
    poll_id = results.get('poll_id', 'N/A')
    question = results.get('question', 'N/A')
    results_data = results.get('results', [])
    
    print(f"Poll #{poll_id}: {question}")
    print("=" * 50)
    
    if not results_data:
        print("No votes cast yet.")
        return
    
    # Sort by vote count (descending)
    sorted_results = sorted(results_data, key=lambda x: x.get('vote_count', 0), reverse=True)
    
    total_votes = sum(option.get('vote_count', 0) for option in results_data)
    print(f"Total votes: {total_votes}")
    print("-" * 30)
    
    for i, option in enumerate(sorted_results, 1):
        option_id = option.get('option_id', 'N/A')
        text = option.get('text', 'N/A')
        vote_count = option.get('vote_count', 0)
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        
        print(f"{i}. {text}")
        print(f"   Votes: {vote_count} ({percentage:.1f}%)")
        print(f"   Option ID: {option_id}")
        print()


def get_vote_token(username: str, password: str, base_url: str = "http://localhost:8000") -> Optional[str]:
    """
    Helper function to get a JWT token for voting by logging in.
    
    Args:
        username (str): Username for login
        password (str): Password for login
        base_url (str): The base URL of the API (default: "http://localhost:8000")
    
    Returns:
        Optional[str]: JWT token on success, None on failure
    """
    url = f"{base_url}/login"
    
    # Prepare form data for login
    data = {
        "username": username,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            print(f"Login failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Login error: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Example 1: Get poll results
    try:
        results = get_poll_results(poll_id=1)
        print_poll_results(results)
    except Exception as e:
        print(f"Error getting results: {e}")
    
    # Example 2: Cast a vote (requires authentication)
    # First, get a token by logging in
    token = get_vote_token("testuser", "testpassword123")
    if token:
        try:
            vote_data = cast_vote(poll_id=1, option_id=2, token=token)
            print(f"Vote cast successfully: {vote_data}")
        except Exception as e:
            print(f"Error casting vote: {e}")
    else:
        print("Failed to get authentication token")
    
    # Example 3: Using error handling functions
    results = get_poll_results_with_error_handling(poll_id=1)
    if results:
        print_poll_results(results)
    
    if token:
        vote_data = cast_vote_with_error_handling(poll_id=1, option_id=1, token=token)
        if vote_data:
            print("Vote cast successfully")
