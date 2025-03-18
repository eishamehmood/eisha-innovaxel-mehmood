from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import random
import string
from datetime import datetime

from database import SessionLocal, create_tables, URL  # Import database setup

app = FastAPI()

# Initialize database tables
create_tables()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request validation
class URLRequest(BaseModel):
    url: str

# Function to generate a random short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Create Short URL and now adding the commit
@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    # Ensure unique short_code
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_url = URL(url=request.url, short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "id": new_url.id,
        "url": new_url.url,
        "shortCode": new_url.short_code,
        "createdAt": new_url.created_at,
        "updatedAt": new_url.updated_at
    }

# Retrieve Original URL add the method to commit
@app.get("/shorten/{short_code}")
def get_original_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Not Found")

    # Increment access count
    url_entry.access_count += 1
    db.commit()

    return {
        "id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.short_code,
        "createdAt": url_entry.created_at,
        "updatedAt": url_entry.updated_at,
        "accessCount": url_entry.access_count
    }

# Update Short URL and now adding the commit
@app.put("/shorten/{short_code}")
def update_short_url(short_code: str, request: URLRequest, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Not Found")

    url_entry.url = request.url
    url_entry.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(url_entry)

    return {
        "id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.short_code,
        "createdAt": url_entry.created_at,
        "updatedAt": url_entry.updated_at
    }

#Delete Short URL
@app.delete("/shorten/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shortened_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Not Found")

    db.delete(url_entry)
    db.commit()
    return

# Get URL Statistics
@app.get("/shorten/{short_code}/stats")
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Not Found")

    return {
        "id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.short_code,
        "createdAt": url_entry.created_at,
        "updatedAt": url_entry.updated_at,
        "accessCount": url_entry.access_count
    }
