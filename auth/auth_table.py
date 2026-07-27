from auth_database import engine, Base

import models

Base.metadata.create_all(bind = engine)


# After running this, we can go and check if the user table has been created. 
# Yes, Ia m seeing it when I run this; SELECT * FROM fastapi_db.users;

# Next, let's run our server, click on the url and go to docus and put somed data
# We have put passwords as 123 but it has been hashed and stored as hashed in the database
# Signup endpoint is working perfect.

# If you try the login, it and wrong details, it will say invalid user name