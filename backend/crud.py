from sqlalchemy.orm import Session
import models
def get_user_by_username(db: Session, username: str):
    """
    Find a user by their username.
    Returns the user object or None if not found.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user(db: Session, user_id: int):
    """
    Find a user by their ID.
    Used in 2FA verification step.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, username: str, hashed_password: str):
    """
    Create a new user in the database.
    Used during registration.
    """
    db_user = models.User(
        username=username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Get the newly created ID etc.
    return db_user


def update_user_2fa_secret(db: Session, user_id: int, secret: str):
    """
    Save the generated TOTP secret for the user (before enabling 2FA).
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.totp_secret = secret
        db.commit()
        db.refresh(user)
    return user


def enable_2fa(db: Session, user_id: int):
    """
    Actually turn on the 2FA flag after user confirms the code.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.is_2fa_enabled = True
        db.commit()
        db.refresh(user)
    return user