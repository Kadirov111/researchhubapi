# ResearchHub API - Authentication and User Management

## Features

- User Registration with Email Verification
- JWT Authentication
- Password Reset
- User Profile Management
- Custom User Model with research-specific fields

## Endpoints

### Authentication

- `POST /api/v1/token/` - Login and obtain JWT token
- `POST /api/v1/token/refresh/` - Refresh JWT token

### User Management

- `POST /api/v1/users/` - Register new user
- `GET /api/v1/users/me/` - Get current user info
- `PATCH /api/v1/users/{id}/` - Update user profile
- `POST /api/v1/users/change_password/` - Change password
- `POST /api/v1/users/request_password_reset/` - Request password reset
- `POST /api/v1/users/confirm_password_reset/` - Confirm password reset
- `POST /api/v1/users/verify_email/` - Verify email with token
- `POST /api/v1/users/resend_verification/` - Resend verification email

## Required Settings

Make sure to configure the following settings in your `settings.py`:

- Custom User Model: `AUTH_USER_MODEL = 'users.User'`
- JWT settings (token lifetimes)
- Email settings (for verification and password reset)
- Frontend URL (for verification and password reset links)


**Kerakli paketlar:**

- Django==4.2.7
- djangorestframework==3.14.0
- djangorestframework-simplejwt==5.3.0
- Pillow==10.0.0  # Profile rasmlar uchun