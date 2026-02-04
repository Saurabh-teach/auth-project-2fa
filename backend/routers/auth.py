from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
import schemas
import crud
import auth
import dependencies

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    return crud.create_user(db=db, username=user.username, hashed_password=hashed_password)


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.is_2fa_enabled:
        return {"requires_2fa": True, "temp_user_id": user.id}
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token/2fa")
def login_with_2fa(data: schemas.TwoFactorVerify, db: Session = Depends(get_db)):
    user = crud.get_user(db, data.user_id)
    if not user or not user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="Invalid request")
    
    if not auth.verify_totp(user.totp_secret, data.code):
        raise HTTPException(status_code=401, detail="Invalid 2FA code")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/2fa/enable")
def enable_2fa(current_user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(get_db)):
    if current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA already enabled")
    
    secret = auth.generate_totp_secret()
    uri = auth.get_totp_uri(current_user.username, secret)
    qr_base64 = auth.generate_qr_base64(uri)
    
    crud.update_user_2fa_secret(db, current_user.id, secret)
    
    return {
        "secret": secret,
        "qr_code": f"data:image/png;base64,{qr_base64}",
        "uri": uri,
        "temp_user_id": current_user.id   # ← ADDED THIS LINE (fixes frontend tempUserId)
    }


@router.post("/2fa/confirm")
def confirm_2fa(
    data: schemas.TwoFactorVerify,
    current_user: schemas.User = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.totp_secret or current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="Invalid state")
    
    if not auth.verify_totp(current_user.totp_secret, data.code):
        raise HTTPException(status_code=401, detail="Invalid code")
    
    crud.enable_2fa(db, current_user.id)
    return {"message": "2FA enabled successfully"}