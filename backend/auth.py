from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
import pyotp
import qrcode
import io
import base64

# IMPORTANT: Change this in production! Use environment variable instead.
SECRET_KEY = "your-super-secret-key-change-this-very-long-random-string-1234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ── 2FA (TOTP) helpers ───────────────────────────────────────────────────────

def generate_totp_secret() -> str:
    """Generate a new random base32 secret for TOTP"""
    return pyotp.random_base32()

def get_totp_uri(username: str, secret: str, issuer_name: str = "MyAuthApp") -> str:
    """Create provisioning URI that can be used in authenticator apps"""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer_name)

def generate_qr_base64(uri: str) -> str:
    """Generate QR code as base64 string (for img src in frontend)"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def verify_totp(secret: str, token: str) -> bool:
    """Verify the 6-digit code entered by user"""
    totp = pyotp.TOTP(secret)
    return totp.verify(token)