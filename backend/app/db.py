import os
from datetime import datetime
import uuid
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Get PostgreSQL connection string from environment variable
db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/tally_subscribers')
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class Subscriber(Base):
    __tablename__ = "subscribers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)
    data = Column(JSON, default={})

class FormSubmission(Base):
    __tablename__ = "form_submissions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    form_id = Column(String, index=True)
    submission_data = Column(JSON)
    received_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Helper function to get database session
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def add_subscriber(email, name=None, data=None):
    """
    Add a new subscriber to the database
    """
    db = get_db()
    
    # Check if subscriber already exists
    existing = db.query(Subscriber).filter(Subscriber.email == email).first()
    
    if existing:
        # Update existing subscriber
        existing.name = name if name else existing.name
        existing.active = True
        if data:
            if existing.data is None:
                existing.data = data
            else:
                existing.data.update(data)
        db.commit()
        subscriber_id = existing.id
    else:
        # Insert new subscriber
        subscriber = Subscriber(
            email=email,
            name=name,
            active=True,
            data=data or {}
        )
        db.add(subscriber)
        db.commit()
        subscriber_id = subscriber.id
        
    db.close()
    return subscriber_id

def get_subscribers(active_only=True):
    """
    Get all subscribers
    """
    db = get_db()
    if active_only:
        subscribers = db.query(Subscriber).filter(Subscriber.active == True).all()
    else:
        subscribers = db.query(Subscriber).all()
    
    # Convert SQLAlchemy objects to dictionaries
    result = [{
        '_id': sub.id,
        'email': sub.email,
        'name': sub.name,
        'subscribed_at': sub.subscribed_at,
        'updated_at': sub.updated_at,
        'active': sub.active,
        'data': sub.data or {}
    } for sub in subscribers]
    
    db.close()
    return result

def unsubscribe(email):
    """
    Mark a subscriber as inactive
    """
    db = get_db()
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if subscriber:
        subscriber.active = False
        db.commit()
    db.close()

def save_form_submission(form_id, submission_data):
    """
    Save a form submission
    """
    db = get_db()
    submission = FormSubmission(
        form_id=form_id,
        submission_data=submission_data
    )
    db.add(submission)
    db.commit()
    submission_id = submission.id
    db.close()
    return submission_id

def get_form_submissions(form_id=None):
    """
    Get form submissions
    """
    db = get_db()
    if form_id:
        submissions = db.query(FormSubmission).filter(FormSubmission.form_id == form_id).all()
    else:
        submissions = db.query(FormSubmission).all()
    
    # Convert SQLAlchemy objects to dictionaries
    result = [{
        '_id': sub.id,
        'form_id': sub.form_id,
        'submission_data': sub.submission_data,
        'received_at': sub.received_at
    } for sub in submissions]
    
    db.close()
    return result
