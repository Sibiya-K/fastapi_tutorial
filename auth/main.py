from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils # we are supporting the supporting files
from auth_database import get_db

# SECRET_KEY/ALGORITHM live in utils.py so the same values sign (here)
# and verify (utils.get_current_user) every token.
SECRET_KEY = utils.SECRET_KEY
ALGORITHM = utils.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Helper function that takes user data
from jose import jwt
from datetime import datetime, timedelta, timezone
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check the user exist or not
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user: 
        raise HTTPException(status_code=400, detail="Username already exist")
    
    # Hash the password
    hashed_pass = utils.hashed_password(user.password)

    # Create new user instance
    # role is intentionally omitted so it always falls back to the
    # models.User default ("user") instead of trusting client input.
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pass
    )

    # Save user in the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the value (excluding password)
    return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email, 'role': new_user.role}

# Signup process is complete, and the user can sign up using this endpoint
# Next we create our login endpoint

from fastapi.security import OAuth2PasswordRequestForm
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
    token_data = {'sub': user.username, 'role': user.role}
    token = create_access_token(token_data)
    
    return {'access_token': token, 'token_type': 'bearer'}

# We can gho ahead and try tpo view these in Swagge URL

@app.get("/protected")
def protected_route(current_user: dict = Depends(utils.get_current_user)):
    return {"message": f"Hello, {current_user['username']} | You accessed a protected route"}

@app.get("/profile")
def profile(current_user: dict = Depends(utils.require_roles(["user", "admin"]))):
    return {"message": f"Profile of {current_user['username']} ({current_user['role']})"}

@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(utils.require_roles(["user"]))):
    return {"message": "Welcome User"}

@app.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(utils.require_roles(["admin"]))):
    return {"message": "Welcome Admin"}

