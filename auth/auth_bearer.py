from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from auth.auth_handler import decode_jwt, decode_jwt_admin


def verify_jwt(token):
    is_token_valid = False

    try:
        payload = decode_jwt(token)
    except:
        payload = None

    if payload:
        is_token_valid = True

    return is_token_valid


def verify_jwt_admin(token):
    is_token_valid = False

    try:
        payload = decode_jwt_admin(token)
    except:
        payload = None

    if payload:
        is_token_valid = True

    return is_token_valid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


class JWTBearerAdmin(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearerAdmin, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerAdmin, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt_admin(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")