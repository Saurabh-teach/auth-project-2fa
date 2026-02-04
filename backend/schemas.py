from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):                  # ← this is the only change
    id: int
    username: str
    is_2fa_enabled: bool

    class Config:
        from_attributes = True

class TwoFactorVerify(BaseModel):
    user_id: int
    code: str
