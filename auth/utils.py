# This is where we hash our passwords, help us verify our password

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated = 'auto')

def hashed_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Now all our support files are read, we go ahead and creat the main file
# When the password has matched, you see the JWT token has been create

import os
from dotenv import load_dotenv # So that we can protect our keys to get to gitbhub
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

load_dotenv() # So that we can use the module

# Single source of truth for JWT settings; main.py imports these from here
# so the token is signed and verified with the same key/algorithm.
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    headers = {"WWW-Authenticate" : "Bearer"}
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "could not validat creditiaol", headers = headers)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credential_exception


    except JWTError:
        raise credential_exception

    return {"username": username, "role": role}

def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission") 
        
        return current_user
    
    return role_checker