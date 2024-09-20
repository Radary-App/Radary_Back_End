
# How to Use the API

This guide explains how to use the  API endpoints available in this project.

## Endpoints

### 1. Sign Up
**URL:** `/signup/`  
**Method:** `POST`  
**Payload:**
```json
{
  "phone_number": "987654321",
  "password": "testpass321",
  "first_name" : "test",
  "last_name" : "test",
  "username" : "testuser"
}
```
**Response:**
```json
{
  "message": "User created successfully"
}
```

### 2. Login
**URL:** `/login/`  
**Method:** `POST`  
**Payload:**
```json
{
  "phone_number": "123456789",
  "password": "testpass123"
}
```
**Response:**
```json
{
  "token": "<your_token>"
}
```

### 3. Create Problem
**URL:** `/problem/create/`  
**Method:** `POST`  
**Authentication:** Token  
**Payload:**
```json
{
  "description": "Problem description",
  "coordinates": "40.748817,-73.985428",
  "photo": "base64-image-data",
  "user_description": "This is a problem",
  
}
```

### 4. Get Problem List (Paginated)
**URL:** `/problem/<int:page_number>/`  #page number e.g : 1.2.3. ...
**Method:** `GET`  
**Authentication:** Token  

### 5. Create Emergency
**URL:** `/emergency/create/`  
**Method:** `POST`  
**Authentication:** Token  
**Payload:**
```json
{
  "description": "Emergency description",
  "coordinates": "40.748817,-73.985428",
}
```

### 6. Get Emergency List (Paginated)
**URL:** `/emergency/<int:page_number>/`  
**Method:** `GET`  
**Authentication:** Token  

### 7. Create Review for Problem
**URL:** `/problem/<int:problem_id>/review/`  
**Method:** `POST`  
**Authentication:** Token  
**Payload:**
```json
{
  "difficulty": 4,
  "comment": "Great work"
}
```

### 8. Update User Profile
**URL:** `/profile/update/`  
**Method:** `PUT`  
**Authentication:** Token  
**Payload:**
```json
{
  "email": "newemail@example.com",
  "phone_number": "987654321",
  "last_name" : "test",
  "first_name" : "test",
  "username" : "testuser",
  "governorate" : "Cairo",
  "markaz" : "Nasr City",
  "image" : "base64-image-data",
  "date_of_birth" : "1990-01-01",
}
```

## Testing

To run automated tests for the API:
```bash
python manage.py test
```
