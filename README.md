# Project Title

Two-Factor Authentication (2FA) App

>
This project is a Two-Factor Authentication (2FA) web application with a backend built using FastAPI (Python) and MySQL, and a separate frontend developed with Vue.js.The backend serves JSON APIs for user authentication and 2FA management, while the frontend handles the user interface and navigation. User credentials and 2FA secrets are stored in a MySQL database.

>
# Objective
The goal of this project is to design and implement a secure authentication system that:
- Supports user registration and login
- Stores passwords securely using hashing
- Allows users to enable Two-Factor Authentication
- Requires OTP verification for 2FA-enabled users
- Provides protected routes for authenticated users
This project demonstrates backend API design, security best practices, database integration, and frontend-backend communication.

# Demo Video
Watch the complete working demo here:
#### drive-link : (https://drive.google.com/file/d/1vfprHcD3i_ClW2_HMfltK4w3KltZCW-O/view?usp=sharing)
---
### The video demonstrates:
- User Registration
- Login without 2FA
- Enabling Two-Factor Authentication
- Scanning QR code with authenticator app
- Login using OTP
- Accessing Dashboard

# Screenshots
- Registration Page
- Login Page
- Dashboard
- Enable 2FA
- OTP Verification

## Tech Stack

### Backend
🔹 FastAPI (Python)
FastAPI is used to build high-performance REST APIs quickly with automatic documentation.
It supports async operations, making backend services fast and scalable.

🔹 MySQL (PyMySQL)
MySQL stores structured application data reliably and efficiently.
PyMySQL allows Python applications to connect and execute SQL queries easily.

🔹 pyotp
pyotp generates time-based one-time passwords for two-factor authentication.
It adds an extra security layer to user login systems.

🔹 qrcode
qrcode generates QR codes for sharing OTP secrets or links.
It simplifies setup of authenticator apps.

🔹 passlib (bcrypt)
passlib securely hashes and verifies passwords.
bcrypt protects against brute-force and rainbow table attacks.

🔹 python-dotenv
Loads environment variables from a .env file.
Keeps sensitive credentials out of source code.

🔹 uvicorn
ASGI server used to run FastAPI applications.
Provides fast, lightweight, and production-ready performance.

🔹 starlette sessions
Manages user sessions and cookies.
Helps maintain login state across requests.

🔹 FastAPI CORS Middleware
Allows frontend and backend to communicate across domains.
Prevents browser CORS errors.

### Frontend
🔹 Vue.js 3
Used to build interactive and reactive user interfaces.
Provides component-based structure and high performance.

🔹 Vue Router
Handles client-side navigation between pages.
Enables single-page application routing.

🔹 Axios
Sends HTTP requests from frontend to backend.
Handles API communication easily.

🔹 Vite
Fast development server and build tool.
Provides instant hot reload and optimized builds.

## Database Setup

This authentication app relies on a MySQL database to store user credentials and related data.

1. Create the Database
2. Create a `users` table for storing user credentials:
   - The table includes:
     - `id` INT
     - `username` VARCHAR(150)
     - `password_hash` VARCHAR(255)
     - `secret` VARCHAR(255)
     - `is_2fa_enabled` BOOLEAN DEFAULT FALSE
     - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
3. Create a `.env` file in the project root directory to store database credentials.
4. Ensure the `.env` file is added to `.gitignore`.
5. The app uses the `pymysql` library to connect to MySQL. The connection is managed via a dependency (`get_db`) in the FastAPI application.
6. Run the FastAPI app using `uvicorn` to ensure the database setup works.
7. Access the registration page via the frontend and attempt to register a user.

## Environment Configuration

Create a `.env` file in the project root (this file must NOT be committed — add it to `.gitignore`). Example `.env` contents:

```
DB_HOST=localhost
DB_USER=twofa_user
DB_PASSWORD=strong_password
DB_NAME=database
SECRET_KEY=a_long_random_secret_for_sessions_or_signing
```

Add `.env` to `.gitignore`:

```
.env
```

Load `.env` in code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
```

## Project Structure

```
     auth-project/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── crud.py
│   ├── routers/
│   │   └── auth.py
│   └── venv/
│
└── frontend/
    ├── src/
    │   ├── stores/auth.js
    │   ├── router/index.js
    │   ├── views/
    │   │   ├── Login.vue
    │   │   ├── Dashboard.vue
    │   │   ├── Setup2FA.vue
    │   └── main.js
    ├── package.json
    └── vite.config.js  
```

## API Design

### Clear Separation of Concerns
- The backend serves JSON APIs instead of rendering HTML, allowing a distinct frontend to consume them.
- Endpoints that retrieve data or forms return JSON (e.g., GET `/register`, GET `/login`).
- Endpoints that perform changes use POST and return JSON with a `redirect` field for frontend navigation (e.g., POST `/register`, POST `/login`).

### HTTP Verbs
- GET: Retrieval of initial form data or dashboard info (e.g., `/register`, `/dashboard`).
- POST: Actions like registration, login, enabling 2FA, and verifying 2FA (e.g., `/register`, `/verify_2fa`).
- GET: Logout action (e.g., `/logout`).

### Protection of Sensitive Flows
- Endpoints modifying authentication state (e.g., `/login`, `/enable_2fa`, `/verify_2fa`) return appropriate JSON responses with `message` and `redirect` fields.
- Success responses include a `redirect` to guide the frontend.
- Failures return a `message` with an error (e.g., "Invalid username or password") and a `redirect` back to the form.

### 2FA Flow (TOTP)
- **User Registration**: User provides username and password. Password is hashed and stored.
- **Enable 2FA**: 
  - User logs in, requests 2FA setup via `/enable_2fa`.
  - Backend generates a TOTP secret (`pyotp.random_base32()`), stores it in `secret`, and returns a QR code (base64 via `qrcode`).
  - User scans the QR code with an authenticator app and submits the first TOTP code.
  - Backend verifies the code with `pyotp.TOTP(otp_secret).verify(code)` and sets `is_2fa_enabled` to `true`.
- **Login with 2FA**: 
  - After verifying username/password, if `is_2fa_enabled` is `true`, the backend redirects to `/verify_2fa`.
  - User enters the TOTP code, which the backend verifies before establishing the session.

## Setup Instructions

### Backend Setup
1. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn pyotp qrcode[pil] pymysql python-dotenv passlib[bcrypt] starlette
   ```
2. Configure `.env` with MySQL credentials.
3. Run the backend:
   ```bash
   uvicorn app:app --host localhost --port 8000 --reload
   ```

### Frontend Setup
1. Navigate to `frontend/`:
   ```bash
   cd version2/frontend
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Run the frontend development server:
   ```bash
   npm run dev
   ```
4. Access the app at `http://localhost:5173/`.

- Test the full flow in the browser at `http://localhost:5173/`.



### Overview
- **Application Components**:
  - **Backend**: FastAPI-based API for user registration, login, and 2FA management.
  - **Frontend**: Vue.js application served via Nginx.
  - **Database**: MySQL 8.0 for storing user data.

- **Software**:
  - Python 3.11 (for local backend development).
  - Node.js and npm (for local frontend development).



## Test the Application
- Frontend Testing
Open the application in your browser: 
  `http://localhost:5173/`
Verify that the user interface loads correctly.

- Backend Testing
Open API documentation:
`http://localhost:8000/docs`
Confirm that all API endpoints are accessible.
#### User Authentication Testing
Register a new user.
Log in using username/password and verify Two-Factor Authentication (2FA).

- Database Verification
Run the following query:
`SELECT * FROM users;`
Verify that user records are stored correctly.

### Conclusion
This project demonstrates a secure Two-Factor Authentication system using FastAPI, MySQL, and Vue.js. It follows best practices for password hashing, OTP-based verification, and frontend-backend separation. The application is accessible at `http://localhost:5173/` (frontend) and `http://localhost:8000` (backend API).


## Use of AI Tools
- GROK
- CHATGPT
