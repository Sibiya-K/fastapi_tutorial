# We must, here, mention all the pydentic that we will use in our file

from pydantic import BaseModel, EmailStr


# Schema for new user create
# Note: role is intentionally NOT accepted from the client here — every
# signup gets the "user" role (models.User.role default). Promoting to
# admin must happen out-of-band (direct DB update or a future admin-only
# endpoint), never via a value the caller supplies.
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for user login
class UserLogin(BaseModel):
    usernam: str
    password: str

# our schema is read, we next create file called utils.