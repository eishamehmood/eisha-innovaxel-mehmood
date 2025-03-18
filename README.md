# URL Shortening Service

## Overview
This project is a RESTful API for a URL shortening service built using **Flask** (Python framework) and **MySQL** (relational database). It allows users to:

- **Create** a short URL for a given long URL.
- **Retrieve** the original URL from a short URL.
- **Update** an existing short URL.
- **Delete** a short URL.
- **View statistics** on the number of times a short URL has been accessed.

## Features
- Create a new short URL using a random, unique short code.
- Retrieve the original URL using the associated short code.
- Update an existing short URL with a new long URL.
- Delete a short URL.
- Statistics: Track and return the number of accesses for each short URL.

## Tech Stack
- **Programming Language & Framework:** Python with Flask
- **Database:** MySQL

## Setup Instructions

### 1. Clone this repository:
```bash
git clone https://github.com/eishamehmood/eisha-innovaxel-mehmood.git
```

### 2. Navigate to the project directory:
```bash
cd eisha-innovaxel-mehmood
```

### 3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Initialize the database:
```bash
flask db upgrade
```

### 5. Start the Flask development server:
```bash
flask run
```

### 6. Access the API endpoints at:
```
http://localhost:5000
```

## API Endpoints

### 1. Create a short URL:
```http
POST /shorten
```
**Request Body:**
```json
{
  "long_url": "https://example.com"
}
```

### 2. Retrieve the original URL using the short code:
```http
GET /shorten/:shortCode
```

### 3. Update an existing short URL with a new long URL:
```http
PUT /shorten/:shortCode
```
**Request Body:**
```json
{
  "long_url": "https://newexample.com"
}
```

### 4. Delete a short URL:
```http
DELETE /shorten/:shortCode
```

### 5. Retrieve the statistics for a given short URL:
```http
GET /shorten/:shortCode/stats
```

