from fastapi import HTTPException, Header,status
from supabase import AuthApiError, SupabaseAuthClient
from gotrue.errors import AuthApiError


def get_current_user(supabase: SupabaseAuthClient, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    try:
        response = supabase.auth.get_user(token)

        if response.user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid or expired token")

        return response.user
    except AuthApiError as e:
        if "token is expired" in str(e):
            raise HTTPException(
                status_code=401,
                detail="Token is expired. Please log in again."
            )
        else:
            # Handle other errors from AuthApiError
            raise HTTPException(
                status_code=401,
                detail=f"Authentication error: {str(e)}"
            )




def get_authenticated_user(authorization: str = Header(None)):
    from main import supabase  # Import here to avoid circular imports

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is required")

    user = get_current_user(supabase, authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authorization token")

    return user  # Return user so other functions can use it
