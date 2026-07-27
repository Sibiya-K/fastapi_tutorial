from fastapi import FastAPI, Depends
from database import get_db, engine
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel

# Let's create our API

app = FastAPI()

class Bookstore(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

@app.post("/books")
def create_book(book: Bookstore, db: Session=Depends(get_db)):
    new_book = model.Book(id = book.id, title = book.title, author = book.author, publish_date = book.publish_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Then we run the above using uvicorn (uvicorn project:app --reload)

# After running the project, it will create the post route.
# You go and test it, and put a book.
# When you get code 200 it means sucess.
# You then test by running code (SELECT * FROM fastapi_db.books;)

# Next we do route to see our books from the URL.
@app.get("/books")
def get_book(db: Session=Depends(get_db)):
    books = db.query(model.Book).all()
    return books

# Next we go to the post, and demostrate posting
# a book, and it shows book added
# When you run SQL it will also show the book in 
# Now in the database

# Next we move to th FastAPI authentication
# Vs Authorization
# Making sure that only specific users can access and use the database; using JWT tokens and secure
# login