# Issue Tracking System

## Overview

This project is an Issue Tracking System built with Django. It includes a custom user model, token-based authentication, and a robust issue management system with AI-generated insights.

## Features

- **Custom User Model**: Extends the default Django user model with additional fields for better customization.
- **Token Authentication**: Manages authentication using token-based methods.
- **Issue Management**: Allows users to report and track issues with varying levels of severity.
- **AI Integration**: Provides AI-generated descriptions, solutions, and severity insights for reported issues.
- **Admin Dashboard**: A dedicated admin interface for managing the system.

## Models

### User

The custom user model extends the default `AbstractUser` model with the following fields:

- `phone_number`: A unique phone number for the user (required for authentication).
- `governorate`: Optional field for specifying the user's governorate.
- `markaz`: Optional field for specifying the user's markaz.
- `date_of_birth`: Optional field for storing the user's date of birth.
- `is_active`: Boolean field indicating if the user is active.
- `is_staff`: Boolean field indicating staff privileges.
- `is_admin`: Boolean field indicating if the user is an admin.
- `created_at`: Timestamp of when the user account was created.
- `updated_at`: Timestamp of when the user account was last updated.

### Token

Manages authentication tokens:

- `user`: Foreign key to the `User` model.
- `token`: The authentication token.
- `created_at`: Timestamp of when the token was created.
- `expired_at`: Timestamp of when the token expires.

### Issue

Tracks reported issues:

- `title`: Title or short description of the issue.
- `description`: A detailed description of the issue.
- `address`: Address where the issue occurred.
- `photo`: Optional image related to the issue.
- `level`: Severity level (`low`, `medium`, `emergency`).
- `status`: Current status (`reported`, `seen`, `solved`).
- `user`: Foreign key to the `User` who reported the issue.
- `created_at`: Timestamp of when the issue was reported.
- `updated_at`: Timestamp of the last status update.

### Review

Manages reviews for solved issues:

- `issue`: Foreign key to the `Issue`.
- `user`: Foreign key to the `User` submitting the review.
- `difficulty`: Integer rating of how difficult it was to solve the issue (1-5 scale).
- `comment`: Optional comment about the solution or overall experience.
- `created_at`: Timestamp of when the review was submitted.

### AI Content

Stores AI-generated insights related to issues:

- `issue`: Foreign key to the `Issue`.
- `ai_description`: AI-generated summary of the issue.
- `ai_solution`: AI-generated proposed solution.
- `ai_danger_level`: AI-assigned danger level.
- `created_at`: Timestamp of when the AI content was generated.

---

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Radary-App/Back_End.git
   cd Back_End


Create a virtual environment and install dependencies:

bash
Copy code
python -m venv .venv
source .venv/bin/activate  # For Linux/macOS
# For Windows
.venv\Scripts\activate
pip install -r requirements.txt
Apply migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Run the development server:

bash
Copy code
python manage.py runserver
Test the API:

bash
Copy code
python manage.py test
API Endpoints
1. Sign Up
URL: /signup/
Method: POST
Payload:

json
Copy code
{
  "phone_number": "01090362980",
  "password": "testpass321",
  "first_name" : "Test",
  "last_name" : "User"
}
Response:

json
Copy code
{
  "message": "User created successfully"
}
2. Login
URL: /login/
Method: POST
Payload:

json
Copy code
{
  "phone_number": "987654321",
  "password": "testpass321"
}
Response:

json
Copy code
{
  "token": "<your_token>"
}
3. Create Issue
URL: /issue/create/
Method: POST
Authentication: Token
Payload:

json
Copy code
{
  "title": "Street light not working",
  "description": "The streetlight in front of my house is not working",
  "address": "123 Main St, Cairo",
  "photo": "base64-encoded-image",
  "level": "medium"
}
Response:

json
Copy code
{
  "message": "Issue created successfully"
}
4. Get Issue List (Paginated)
URL: /issues/<int:page_number>/
Method: GET
Authentication: Token
Response:

json
Copy code
[
  page_number:
  {
    "id": 1,
    "title": "Street light not working",
    "status": "reported",
    "level": "medium",
    "created_at": "2023-09-01T12:34:56Z"
  },
  ...
]
5. Create Emergency
URL: /emergency/create/
Method: POST
Authentication: Token
Payload:

json
Copy code
{
  "title": "Building collapse",
  "description": "A building collapsed near my house",
  "address": "456 Elm St, Alexandria",
  "photo": "base64-encoded-image",
  "level": "emergency"
}
Response:

json
Copy code
{
  "message": "Emergency reported successfully"
}
6. Get Emergency List (Paginated)
URL: /emergencies/<int:page_number>/
Method: GET
Authentication: Token
Response:

json
Copy code
[
  {
    "id": 2,
    "title": "Building collapse",
    "status": "reported",
    "level": "emergency",
    "created_at": "2023-09-01T13:45:00Z"
  },
  ...
]
7. Create Review for Solved Issue
URL: /issue/<int:issue_id>/review/
Method: POST
Authentication: Token
Payload:

json
Copy code
{
  "is_solved":"T",
  "difficulty": "F",
  "comment": "The issue was solved quickly"
}
Response:

json
Copy code
{
  "message": "Review submitted successfully"
}
8. Update User Profile
URL: /profile/update/
Method: PUT
Authentication: Token
Payload:

json
Copy code
{
  "email": "newemail@example.com",
  "phone_number": "987654321",
  "first_name": "Test",
  "last_name": "User",
  "username": "newuser",
  "governorate": "Cairo",
  "markaz": "Nasr City",
  "date_of_birth": "1990-01-01",
  "photo": "base64-encoded-image"
}
Response:

json
Copy code
{
  "message": "Profile updated successfully"
}
Running Tests
To run the automated test suite:

bash
Copy code
python manage.py test
License
This project is licensed under the MIT License.