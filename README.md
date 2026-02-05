🔐 Two-Factor Authentication (2FA) App

A full-stack Two-Factor Authentication (2FA) web application built using FastAPI (Python) for the backend and Vue.js 3 for the frontend.

The application allows users to register, log in, and optionally enable Time-based One-Time Password (TOTP) authentication using authenticator apps such as Google Authenticator or Authy.

🎯 Objective

The goal of this project is to design and implement a secure authentication system that:

Supports user registration and login

Stores passwords securely using hashing

Allows users to enable Two-Factor Authentication

Requires OTP verification for 2FA-enabled users

Provides protected routes for authenticated users

This project demonstrates backend API design, security best practices, database integration, and frontend-backend communication.

🎥 Demo Video

Watch the complete working demo here:

https://your-demo-video-link-here


The video demonstrates:

User Registration

Login without 2FA

Enabling Two-Factor Authentication

Scanning QR code with authenticator app

Login using OTP

Accessing Dashboard

🖼️ Screenshots
🔹 Registration Page

🔹 Login Page

🔹 Dashboard

🔹 Enable 2FA

🔹 OTP Verification

🧰 Tech Stack
Backend

FastAPI (Python)

MySQL (PyMySQL)

pyotp

qrcode

passlib (bcrypt)

python-dotenv

uvicorn

starlette sessions

fastapi CORS middleware

Frontend

Vue.js 3

Vue Router

Axios

Vite

🗄️ Database Setup

Create database:

CREATE DATABASE twofa_db;


Create table:

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE,
    password_hash VARCHAR(255),
    secret VARCHAR(255),
    is_2fa_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

🔐 Environment Configuration

Create .env file in root:

DB_HOST=localhost
DB_USER=twofa_user
DB_PASSWORD=strong_password
DB_NAME=twofa_db
SECRET_KEY=a_long_random_secret


Add to .gitignore:

.env

📁 Project Structure
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

🔁 API Design
Method	Endpoint	Description
POST	/register	Register user
POST	/login	Login user
POST	/enable-2fa	Generate QR
POST	/verify-2fa	Verify OTP
GET	/logout	Logout
Sample Response
{
  "message": "Success",
  "redirect": "/dashboard"
}

🔐 2FA Flow
Registration

User enters username & password

Password hashed and stored

Enable 2FA

Backend generates secret

QR code created

User scans QR

User enters OTP

Backend verifies and enables 2FA

Login With 2FA

Username & password verified

OTP required

OTP validated

Dashboard accessible

⚙️ Backend Setup
pip install fastapi uvicorn pyotp qrcode[pil] pymysql python-dotenv passlib[bcrypt] starlette


Run backend:

uvicorn main:app --reload


Backend URL:

http://localhost:8000


API Docs:

http://localhost:8000/docs

🎨 Frontend Setup
cd frontend
npm install
npm run dev


Frontend URL:

http://localhost:5173

🧪 Testing Checklist

Register user

Login user

Enable 2FA

Scan QR

Enter OTP

Logout

Login with OTP

🔒 Security Practices

Password hashing with bcrypt

Secrets stored securely

Environment variables

OTP-based authentication

🤖 Use of AI Tools

AI tools such as ChatGPT and Grok were used for:

Understanding TOTP concepts

Generating boilerplate code

Debugging issues

Writing documentation

All final logic and integration were implemented manually.

🚀 Future Enhancements

JWT authentication

Email verification

Password reset

Rate limiting

UI enhancements
