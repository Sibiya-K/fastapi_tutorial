from database import engine, Base

import model

Base.metadata.create_all(bind = engine)

# all is ready, we can run the code, by coding; python create_table.py

# Next, the table is now there, we must insert data into our table
# Let create another file called, project.py
