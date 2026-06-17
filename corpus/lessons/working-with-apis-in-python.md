---
title: "Working with APIs in Python"
subject: "00_Basics"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Working with APIs in Python

## Basic GET Request
```python
import requests

# Simple GET
response = requests.get("https://api.example.com/users")

# Check status
if response.status_code == 200:
    data = response.json()  # Parse JSON
    print(data)
else:
    print(f"Error: {response.status_code}")
```

## Common HTTP Methods
```python
import requests

# GET - retrieve data
response = requests.get("https://api.example.com/users")

# POST - create data
data = {"name": "Billy", "age": 30}
response = requests.post("https://api.example.com/users", json=data)

# PUT - update entire resource
response = requests.put("https://api.example.com/users/1", json=data)

# PATCH - partial update
response = requests.patch("https://api.example.com/users/1", json={"age": 31})

# DELETE - remove resource
response = requests.delete("https://api.example.com/users/1")
```

## Headers and Authentication
```python
# Custom headers
headers = {
    "User-Agent": "MyApp/1.0",
    "Accept": "application/json"
}
response = requests.get(url, headers=headers)

# API Key authentication
headers = {"Authorization": "Bearer YOUR_API_KEY"}
response = requests.get(url, headers=headers)

# Basic auth
from requests.auth import HTTPBasicAuth
response = requests.get(url, auth=HTTPBasicAuth("username", "password"))

# Or simpler
response = requests.get(url, auth=("username", "password"))
```

## Query Parameters
```python
# Manual
url = "https://api.example.com/search?q=python&limit=10"
response = requests.get(url)

# Better - use params dict
params = {
    "q": "python",
    "limit": 10,
    "sort": "newest"
}
response = requests.get("https://api.example.com/search", params=params)
```

## Handling JSON
```python
import json

# Parse JSON response
response = requests.get(url)
data = response.json()

# Parse JSON string
json_string = '{"name": "Billy", "age": 30}'
data = json.loads(json_string)

# Create JSON string
data = {"name": "Billy", "age": 30}
json_string = json.dumps(data, indent=2)

# Read JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Write JSON file
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
```

## Error Handling
```python
import requests

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Connection error")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

## Response Object
```python
response = requests.get(url)

# Status code
print(response.status_code)  # 200, 404, 500, etc.

# Check if successful
if response.ok:  # True for 200-299
    print("Success")

# Response content
text = response.text  # Raw text
data = response.json()  # Parsed JSON
binary = response.content  # Binary data

# Response headers
print(response.headers)
print(response.headers["Content-Type"])

# Request details
print(response.request.url)
print(response.request.headers)
```

## Sessions (For multiple requests)
```python
# Use session to persist cookies, headers
session = requests.Session()
session.headers.update({"Authorization": "Bearer TOKEN"})

# All requests use same headers
response1 = session.get("https://api.example.com/users")
response2 = session.get("https://api.example.com/posts")

session.close()

# Or use context manager
with requests.Session() as session:
    session.headers.update({"Auth": "token"})
    response = session.get(url)
```

## File Uploads
```python
# Upload file
files = {"file": open("document.pdf", "rb")}
response = requests.post(url, files=files)

# With additional data
files = {"file": open("image.png", "rb")}
data = {"description": "My image"}
response = requests.post(url, files=files, data=data)

# Custom filename
files = {"file": ("custom_name.txt", open("file.txt", "rb"))}
response = requests.post(url, files=files)
```

## Common Patterns
```python
# Retry logic
def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            print(f"Retry {attempt + 1}/{max_retries}")
            time.sleep(2 ** attempt)  # Exponential backoff

# Pagination
def fetch_all_pages(base_url):
    all_data = []
    page = 1
    
    while True:
        response = requests.get(f"{base_url}?page={page}")
        data = response.json()
        
        if not data["results"]:
            break
        
        all_data.extend(data["results"])
        page += 1
    
    return all_data

# Rate limiting
import time

def rate_limited_request(url, calls_per_second=2):
    time.sleep(1 / calls_per_second)
    return requests.get(url)
```

## Working with Different APIs
```python
# REST API
def get_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

def create_user(data):
    response = requests.post("https://api.example.com/users", json=data)
    return response.json()

# GraphQL API
def graphql_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    response = requests.post(
        "https://api.example.com/graphql",
        json=payload
    )
    return response.json()
```

## Testing APIs (Mock responses)
```python
# For testing without actual API calls
from unittest.mock import Mock, patch

def test_get_user():
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Billy"}
    
    with patch("requests.get", return_value=mock_response):
        result = get_user(1)
        assert result["name"] == "Billy"
```

## Quick Tips for Tests
- Use `requests` library (not urllib - too low-level)
- Always set `timeout` to avoid hanging
- Use `.json()` to parse JSON responses
- Use `params` dict instead of manual URL building
- `raise_for_status()` to catch HTTP errors
- Sessions for multiple requests to same API
- Handle errors with try/except
- Use environment variables for API keys

## Common API Patterns in Tests
```python
# Fetch and process data
def get_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        return [repo["name"] for repo in repos]
    return []

# Post data and get response
def create_post(title, body):
    url = "https://jsonplaceholder.typicode.com/posts"
    data = {"title": title, "body": body, "userId": 1}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        return response.json()
    return None

# Simple weather API
def get_weather(city):
    api_key = "YOUR_KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial"
    }
    
    response = requests.get(url, params=params)
    return response.json() if response.ok else None
```

## Environment Variables for API Keys
```python
import os

# Set in environment or .env file
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not set")

headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers)
```

---

## Related Notes
- [Python File IO Essentials](Python-File-IO-Essentials)
- [Python Error Handling](Python-Error-Handling)
- [Python Dictionaries & Sets](Python-Dictionaries-&-Sets)
- [Working with JSON](Working-with-JSON)
- [Environment Variables](Environment-Variables)
- [API Authentication Patterns](API-Authentication-Patterns)
