# users.py - you can leave this empty for now or add later
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

# Example future endpoint (commented)
# @router.get("/me")
# def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_user)):
#     return current_user