# Issue Tracking System

## Overview

This project is an Issue Tracking System built with Django. It includes a custom user model, token-based authentication, and an issue management system with AI-generated insights.

## Features

- **Custom User Model**: Extends the default Django user model with additional fields and features.
- **Token Authentication**: Manages authentication using tokens.
- **Issue Management**: Allows users to report issues with various levels and statuses.
- **Admin Dashboard**: Provides a model for admin-specific data.
- **AI Integration**: Stores AI-generated content related to issues.

## Models

### User

The custom user model extends the default `AbstractUser` model with additional fields:

- `is_admin`: Boolean field to denote if the user is an admin.
- `created_at`: Timestamp of when the user was created.
- `first_name`: Optional first name.
- `last_name`: Optional last name.
- `email`: Unique email address.
- `is_active`: Boolean field to denote if the user is active.
- `is_staff`: Boolean field to denote if the user has staff privileges.
- `password`: User password (stored as a char field).
- `last_login`: Timestamp of the last login.
- `governorate`: Optional field for governorate.
- `markaz`: Optional field for markaz.
- `date_of_birth`: Optional field for date of birth.
- `phone_number`: Optional field for phone number.

### Token

Stores authentication tokens for users:

- `user`: Foreign key to the `User` model.
- `token`: The authentication token.

### Issue

Manages reported issues:

- `title`: Title of the issue.
- `description`: Detailed description of the issue.
- `address`: Address where the issue occurred.
- `photo`: Optional photo related to the issue.
- `level`: Severity level of the issue (`low`, `medium`, `emergency`).
- `user`: Foreign key to the `User` model who reported the issue.
- `status`: Current status of the issue (`reported`, `reported and seen`, `reported and seen and solved`).

### AI

Stores AI-generated content related to issues:

- `issue`: One-to-one relationship with the `Issue` model.
- `ai_description`: AI-generated description.
- `ai_solution`: AI-generated solution.
- `ai_danger_level`: AI-assigned danger level.
## Installation and Setup



1. **Clone the repository**
   ```bash
   git clone https://github.com/Radary-App/Back_End.git
   cd Back_End 
   ```

2. **Create VE and Install Dependencies**
   ```bash
   python -m venv .venv
   cd venv/Scripts
   activate
   cd ../..
   pip install -r requirements.txt
      ```
2. **Apply migrations** 
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Run the development server** 
   ```bash
   python manage.py runserver
   ```
4. **Test the API**
   ```bash
    python manage.py test core
   ```

### API Endpoints
- `POST /signup`: Register a new user.
- `POST /login`: Authenticate a user and retrieve a token.
- `POST /create_problem`: Submit a problem report.
- `GET /browse_problems`: Retrieve a list of problems.
- `POST /create_emergency`: Submit an emergency report.
- `GET /browse_emergencies`: Retrieve a list of emergencies.
- `POST /problem_review/{id}`: Submit a review for a specific problem.
- `PUT /profile`: Update user profile information.

## Running Tests
To run the test suite, use:
# License
This project is licensed under the MIT License.