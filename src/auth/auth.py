from fastapi import HTTPException, Header,status
from supabase import SupabaseAuthClient


def get_current_user(supabase: SupabaseAuthClient, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]

    response = supabase.auth.get_user(token)

    if response.user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid or expired token")

    return response.user
